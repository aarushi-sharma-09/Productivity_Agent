import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, Calendar, MessageSquare, List, CheckCircle2, 
  AlertCircle, Clock, User, ArrowUpRight, ArrowDownRight, Info, ShieldCheck, ArrowRight
} from 'lucide-react';
import { format, parseISO } from 'date-fns';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const Badge = ({ children, type }) => {
  const styles = {
    open: "bg-indigo-500/15 text-indigo-300 border border-indigo-500/30",
    done: "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30",
    overdue: "bg-red-500/15 text-red-300 border border-red-500/30",
    ambiguous: "bg-amber-500/15 text-amber-300 border border-amber-500/30",
    high: "bg-emerald-500/10 text-emerald-300 border border-emerald-500/20",
    medium: "bg-amber-500/10 text-amber-300 border border-amber-500/20",
    low: "bg-red-500/10 text-red-300 border border-red-500/20",
  };
  return <span className={`badge ${styles[type] || styles.open}`}>{children}</span>;
};

const CommitmentCard = ({ c }) => {
  const status = c.status || 'open';
  const dir = c.direction || '';
  const ambiguous = c.ambiguous_owner;
  
  const statusMap = {
    open: { label: "Open", key: "open" },
    done: { label: "Done", key: "done" },
    overdue: { label: "Overdue", key: "overdue" },
    ambiguous_owner: { label: "Owner Unclear", key: "ambiguous" }
  };
  
  const dirMap = {
    arjun_owes: { label: "My action", icon: <ArrowUpRight size={14} className="text-blue-400" /> },
    arjun_waiting_on: { label: "Waiting on", icon: <ArrowDownRight size={14} className="text-purple-400" /> },
    fyi: { label: "FYI", icon: <Info size={14} className="text-slate-400" /> }
  };

  const sl = statusMap[status]?.label || status;
  const sk = statusMap[status]?.key || "open";
  const { label: dirLabel, icon: dirIcon } = dirMap[dir] || { label: dir };
  
  const cardClass = status === 'overdue' ? 'status-overdue' :
                    status === 'done' ? 'status-done' :
                    status === 'ambiguous_owner' ? 'status-ambiguous' :
                    dir === 'arjun_waiting_on' ? 'status-waiting' : 'status-open';

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }} 
      animate={{ opacity: 1, y: 0 }}
      className={`glass-card p-5 mb-4 ${cardClass}`}
    >
      <div className="flex items-start gap-2 mb-2 flex-wrap">
        <span className="font-semibold text-slate-200 flex-1">{c.description}</span>
        <div className="flex gap-2">
          <Badge type={sk}>{sl}</Badge>
          <Badge type={c.confidence}>{c.confidence}</Badge>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-4 items-center text-[0.78rem] text-slate-400 mt-2">
        <span className="flex items-center gap-1.5">{dirIcon} {dirLabel}</span>
        <span className="text-slate-600">•</span>
        <span className="flex items-center gap-1.5"><User size={12}/> {c.counterparty || "—"}</span>
        
        {c.deadline_current && (
          <>
            <span className="text-slate-600">•</span>
            <span className={`flex items-center gap-1.5 font-semibold ${status === 'overdue' ? 'text-red-400' : 'text-amber-500'}`}>
              <Clock size={12}/> {format(parseISO(c.deadline_current), 'd MMM · h:mm a')}
            </span>
          </>
        )}
      </div>

      {ambiguous && (
        <div className="mt-3 text-xs text-amber-500 flex items-center gap-1.5">
          <AlertCircle size={14} /> Ownership unresolved — not assigned to any party
        </div>
      )}

      {c.evidence?.length > 0 && (
        <div className="mt-3 text-[0.65rem] text-slate-500 italic tracking-wide">
          Sources: {c.evidence.join(' · ')}
        </div>
      )}
    </motion.div>
  );
};

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [tab, setTab] = useState('brief');
  const [dateStr, setDateStr] = useState('2026-09-23');
  const [loading, setLoading] = useState(false);
  const [brief, setBrief] = useState(null);
  const [ledger, setLedger] = useState(null);
  const [error, setError] = useState(null);
  
  // Chat state
  const [chat, setChat] = useState([]);
  const [input, setInput] = useState('');
  const [qaLoading, setQaLoading] = useState(false);

  const loadData = async () => {
    try {
      const [briefRes, ledgerRes] = await Promise.all([
        fetch(`${API_URL}/brief?date=${dateStr}`),
        fetch(`${API_URL}/ledger?date=${dateStr}`)
      ]);
      const bd = await briefRes.json();
      const ld = await ledgerRes.json();
      
      if (bd.status === 'success') setBrief(bd.data);
      if (ld.status === 'success') setLedger(ld.data);
      if (bd.status === 'no_ledger') {
        setBrief(null); setLedger(null);
      }
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => { loadData(); }, [dateStr]);

  const rebuild = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/rebuild`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date_str: dateStr })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'API Error');
      await loadData();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const askQ = async (q) => {
    if (!q) return;
    setChat(prev => [...prev, { role: 'user', content: q }]);
    setInput('');
    setQaLoading(true);
    try {
      const res = await fetch(`${API_URL}/qa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, date_str: dateStr })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);
      setChat(prev => [...prev, { role: 'ai', content: data.answer }]);
    } catch (e) {
      setChat(prev => [...prev, { role: 'ai', content: `❌ Error: ${e.message}` }]);
    } finally {
      setQaLoading(false);
    }
  };

  const handleLogin = () => {
    setLoginLoading(true);
    setTimeout(() => {
      setIsAuthenticated(true);
      setLoginLoading(false);
    }, 1200);
  };

  if (!isAuthenticated) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#06060f] overflow-hidden relative">
        <div className="fixed inset-0 pointer-events-none z-0 mix-blend-screen opacity-60">
          <div className="absolute top-[20%] left-[20%] w-[40%] h-[40%] rounded-full bg-indigo-500/20 blur-[120px] animate-aurora" />
          <div className="absolute bottom-[20%] right-[20%] w-[40%] h-[40%] rounded-full bg-violet-500/20 blur-[120px] animate-aurora" style={{animationDelay: '-5s'}} />
        </div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-10 max-w-md w-full z-10 text-center"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-500/20 text-indigo-400 mb-6 border border-indigo-500/30">
            <ShieldCheck size={32} />
          </div>
          
          <h1 className="text-3xl font-bold text-slate-200 mb-2">Veridian Corp</h1>
          <p className="text-slate-400 text-sm mb-8">Executive Productivity Agent SSO</p>
          
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 mb-8 text-left backdrop-blur-md">
            <div className="text-xs text-slate-500 font-bold uppercase tracking-widest mb-1">Authenticating As</div>
            <div className="font-semibold text-slate-200">Arjun Malhotra</div>
            <div className="text-xs text-slate-400">VP Sales · arjun.malhotra@veridian-corp.example</div>
          </div>
          
          <button 
            onClick={handleLogin}
            disabled={loginLoading}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-indigo-500 to-violet-500 hover:from-indigo-600 hover:to-violet-600 text-white rounded-xl py-3.5 font-semibold transition-all shadow-[0_0_20px_rgba(99,102,241,0.3)] disabled:opacity-70"
          >
            {loginLoading ? 'Authenticating...' : <>Access Agent Dashboard <ArrowRight size={18} /></>}
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 pointer-events-none z-0 mix-blend-screen opacity-60">
        <div className="absolute top-[20%] left-[10%] w-[40%] h-[40%] rounded-full bg-indigo-500/20 blur-[120px] animate-aurora" />
        <div className="absolute top-[10%] right-[10%] w-[35%] h-[35%] rounded-full bg-violet-500/20 blur-[100px] animate-aurora" style={{animationDelay: '-5s'}} />
        <div className="absolute bottom-[20%] left-[30%] w-[40%] h-[40%] rounded-full bg-emerald-500/10 blur-[100px] animate-aurora" style={{animationDelay: '-10s'}} />
      </div>

      {/* Sidebar */}
      <div className="w-72 bg-white/[0.02] backdrop-blur-2xl border-r border-white/5 shadow-2xl z-10 flex flex-col">
        <div className="p-8 text-center">
          <div className="text-4xl mb-2 animate-pulse-glow"><Zap className="inline-block text-indigo-400" size={32} /></div>
          <h1 className="text-lg font-bold bg-gradient-to-br from-indigo-300 to-violet-300 bg-clip-text text-transparent">ExecBrief</h1>
          <p className="text-[0.65rem] text-slate-500 uppercase tracking-widest mt-1">Productivity Agent</p>
        </div>
        
        <div className="px-6 flex-1">
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 mb-6 backdrop-blur-md">
            <div className="font-semibold text-sm text-slate-200">Arjun Malhotra</div>
            <div className="text-xs text-slate-400 mt-1">VP Sales · Veridian Corp</div>
          </div>

          <label className="text-[0.65rem] font-bold text-slate-500 uppercase tracking-widest mb-2 block">Brief Date</label>
          <input 
            type="date" 
            value={dateStr}
            onChange={e => setDateStr(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-lg p-2.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500/50 mb-6"
          />

          <hr className="border-white/5 mb-6" />

          <button 
            onClick={rebuild}
            disabled={loading}
            className="w-full bg-gradient-to-br from-indigo-500/20 to-violet-500/20 hover:from-indigo-500/30 hover:to-violet-500/30 border border-indigo-500/30 text-indigo-300 rounded-xl py-3 text-sm font-semibold transition-all shadow-[0_0_20px_rgba(99,102,241,0.15)] disabled:opacity-50"
          >
            {loading ? 'Running...' : '🔄 Rebuild Ledger'}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto z-10 relative scroll-smooth">
        <div className="max-w-6xl mx-auto p-10 pb-24">
          
          {error && (
            <div className="glass-card !border-l-red-500/80 mb-8 p-5 bg-red-500/5">
              <div className="text-red-400 font-bold mb-2 flex items-center gap-2">
                <AlertCircle /> Pipeline Error
              </div>
              <div className="text-sm text-slate-300">{error}</div>
            </div>
          )}

          {/* Tabs header */}
          <div className="flex gap-2 p-1.5 bg-white/5 border border-white/10 rounded-2xl w-fit backdrop-blur-lg mb-10">
            {[
              { id: 'brief', icon: <Calendar size={16}/>, label: 'Daily Brief' },
              { id: 'qa', icon: <MessageSquare size={16}/>, label: 'Ask Arjun' },
              { id: 'ledger', icon: <List size={16}/>, label: 'Full Ledger' }
            ].map(t => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  tab === t.id ? 'bg-indigo-500/25 text-indigo-300 shadow-lg' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                {t.icon} {t.label}
              </button>
            ))}
          </div>

          {!brief && tab !== 'qa' && (
            <div className="text-center p-20 glass-card">
              <AlertCircle size={48} className="mx-auto text-slate-500 mb-4" />
              <h2 className="text-xl font-bold text-slate-200 mb-2">No ledger found</h2>
              <p className="text-slate-400 text-sm">Click Rebuild Ledger in the sidebar to run the extraction pipeline.</p>
            </div>
          )}

          {/* TAB: DAILY BRIEF */}
          {tab === 'brief' && brief && (
            <AnimatePresence mode="wait">
              <motion.div initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}>
                <div className="mb-10">
                  <h1 className="text-4xl font-extrabold bg-gradient-to-r from-slate-200 to-indigo-300 bg-clip-text text-transparent mb-2">
                    Daily Brief
                  </h1>
                  <p className="text-slate-400">{format(parseISO(dateStr), 'EEEE, d MMMM yyyy')}</p>
                </div>

                <div className="grid grid-cols-4 gap-4 mb-10">
                  {[
                    { label: 'My Actions', val: (brief.my_actions?.length||0) + (brief.overdue?.length||0) },
                    { label: '🔴 Overdue', val: brief.overdue?.length||0 },
                    { label: '🟣 Waiting On', val: brief.waiting_on?.length||0 },
                    { label: '🟠 Needs Owner', val: brief.ambiguous?.length||0 }
                  ].map((m, i) => (
                    <div key={i} className="glass-card p-5">
                      <div className="text-[0.65rem] font-bold text-slate-500 uppercase tracking-widest mb-2">{m.label}</div>
                      <div className="text-3xl font-bold text-slate-200">{m.val}</div>
                    </div>
                  ))}
                </div>

                <div className="flex gap-8">
                  <div className="flex-[3]">
                    {brief.overdue?.length > 0 && (
                      <div className="mb-8">
                        <div className="flex items-center gap-2 mb-4 px-4 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-red-300 text-xs font-bold uppercase tracking-wider">
                          🔴 Overdue <span className="ml-auto bg-white/10 px-2 py-0.5 rounded-full">{brief.overdue.length}</span>
                        </div>
                        {brief.overdue.map(c => <CommitmentCard key={c.id} c={c} />)}
                      </div>
                    )}
                    
                    <div className="mb-8">
                      <div className="flex items-center gap-2 mb-4 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg text-blue-300 text-xs font-bold uppercase tracking-wider">
                        🔵 My Actions Today <span className="ml-auto bg-white/10 px-2 py-0.5 rounded-full">{brief.my_actions?.length||0}</span>
                      </div>
                      {brief.my_actions?.map(c => <CommitmentCard key={c.id} c={c} />) || <p className="text-slate-500 text-sm p-4">No actions due today.</p>}
                    </div>

                    <div className="mb-8">
                      <div className="flex items-center gap-2 mb-4 px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-lg text-purple-300 text-xs font-bold uppercase tracking-wider">
                        🟣 Waiting On <span className="ml-auto bg-white/10 px-2 py-0.5 rounded-full">{brief.waiting_on?.length||0}</span>
                      </div>
                      {brief.waiting_on?.map(c => <CommitmentCard key={c.id} c={c} />) || <p className="text-slate-500 text-sm p-4">Nothing waiting.</p>}
                    </div>
                  </div>

                  <div className="flex-[2]">
                    <div className="mb-8">
                      <div className="flex items-center gap-2 mb-4 px-4 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-300 text-xs font-bold uppercase tracking-wider">
                        🟠 Needs Ownership <span className="ml-auto bg-white/10 px-2 py-0.5 rounded-full">{brief.ambiguous?.length||0}</span>
                      </div>
                      {brief.ambiguous?.map(c => <CommitmentCard key={c.id} c={c} />) || <p className="text-slate-500 text-sm p-4">All clear.</p>}
                    </div>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          )}

          {/* TAB: Q&A */}
          {tab === 'qa' && (
            <div className="max-w-3xl mx-auto flex flex-col h-[70vh]">
              <div className="mb-6">
                <h1 className="text-3xl font-bold text-slate-200 mb-2">Ask About Commitments</h1>
                <p className="text-slate-400 text-sm">Grounded strictly in the {dateStr} ledger state.</p>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {["What did I promise Raghav?", "What needs action today?", "Who owns the Mumbai lease?", "Is the expense report done?"].map((q, i) => (
                  <button key={i} onClick={() => askQ(q)} className="px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-slate-300 hover:bg-indigo-500/20 hover:text-indigo-300 transition-colors">
                    {q}
                  </button>
                ))}
              </div>

              <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2">
                {chat.map((m, i) => (
                  <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`p-4 rounded-2xl max-w-[85%] backdrop-blur-md ${m.role === 'user' ? 'bg-indigo-500/20 border border-indigo-500/30 rounded-br-sm' : 'bg-white/5 border border-white/10 rounded-tl-sm'}`}>
                      <div className="text-[0.65rem] font-bold uppercase tracking-wider text-slate-500 mb-1">
                        {m.role === 'user' ? 'You' : 'ExecBrief AI'}
                      </div>
                      <div className="text-sm text-slate-200 whitespace-pre-wrap">{m.content}</div>
                    </div>
                  </div>
                ))}
                {qaLoading && (
                  <div className="flex justify-start">
                    <div className="p-4 rounded-2xl bg-white/5 border border-white/10 rounded-tl-sm">
                      <div className="text-sm text-slate-400 animate-pulse">Thinking...</div>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex gap-2">
                <input 
                  type="text" 
                  value={input} 
                  onChange={e=>setInput(e.target.value)} 
                  onKeyDown={e => e.key === 'Enter' && askQ(input)}
                  placeholder="Ask a question..."
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500/50 backdrop-blur-md"
                />
                <button onClick={() => askQ(input)} disabled={!input || qaLoading} className="bg-indigo-500 text-white px-6 py-3 rounded-xl font-medium disabled:opacity-50">
                  Send
                </button>
              </div>
            </div>
          )}

          {/* TAB: LEDGER */}
          {tab === 'ledger' && ledger && (
            <div>
              <div className="mb-6">
                <h1 className="text-3xl font-bold text-slate-200 mb-2">Raw Ledger</h1>
                <p className="text-slate-400 text-sm">All extracted and deduplicated commitments.</p>
              </div>
              
              <div className="space-y-4">
                {ledger.commitments.map(c => <CommitmentCard key={c.id} c={c} />)}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
