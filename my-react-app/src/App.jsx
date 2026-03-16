import { useState, useRef, useEffect } from 'react';
import './App.css';

function EquationSolver() {
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const aRef = useRef(null);

  useEffect(() => {
    aRef.current?.focus();
  }, []);

  const validate = () => {
    if (a.trim() === '' || b.trim() === '') {
      setError('Vui lòng nhập đầy đủ hệ số a và b.');
      return false;
    }
    if (isNaN(Number(a)) || isNaN(Number(b))) {
      setError('Dữ liệu nhập vào không hợp lệ. Vui lòng nhập số.');
      return false;
    }
    setError('');
    return true;
  };

  const solve = () => {
    if (!validate()) return;
    
    const numA = Number(a);
    const numB = Number(b);
    
    if (numA === 0) {
      if (numB === 0) {
        setResult('Phương trình vô số nghiệm.');
      } else {
        setResult('Phương trình vô nghiệm.');
      }
    } else {
      const x = -numB / numA;
      setResult(`x = ${x}`);
    }
  };

  const reset = () => {
    setA('');
    setB('');
    setResult(null);
    setError('');
    aRef.current?.focus();
  };

  return (
    <div className="component-card glass-panel fade-in">
      <h2>Phương trình bậc nhất (ax + b = 0)</h2>
      
      {error && <div className="alert error">{error}</div>}
      
      <div className="form-group">
        <label>Hệ số a</label>
        <input 
          ref={aRef}
          value={a} 
          onChange={e => setA(e.target.value)} 
          type="text" 
          placeholder="Nhập a" 
          className={error && isNaN(Number(a)) && a !== '' ? 'invalid' : ''}
        />
      </div>
      
      <div className="form-group">
        <label>Hệ số b</label>
        <input 
          value={b} 
          onChange={e => setB(e.target.value)} 
          type="text" 
          placeholder="Nhập b" 
          className={error && isNaN(Number(b)) && b !== '' ? 'invalid' : ''}
        />
      </div>
      
      <div className="action-buttons">
        <button className="btn primary block" onClick={solve}>Giải Phương Trình</button>
        <button className="btn secondary block" onClick={reset}>Reset</button>
      </div>
      
      {result !== null && (
        <div className="result-panel box-up">
          <h3>Kết quả:</h3>
          <p className="result-text">{result}</p>
        </div>
      )}
    </div>
  );
}

function Calculator() {
  const [num1, setNum1] = useState('');
  const [num2, setNum2] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const num1Ref = useRef(null);

  useEffect(() => {
    num1Ref.current?.focus();
  }, []);

  const validate = () => {
    if (num1.trim() === '' || num2.trim() === '') {
      setError('Vui lòng nhập đầy đủ 2 số.');
      return false;
    }
    if (isNaN(Number(num1)) || isNaN(Number(num2))) {
      setError('Dữ liệu nhập vào không hợp lệ. Vui lòng nhập số.');
      return false;
    }
    setError('');
    return true;
  };

  const calculate = (operator) => {
    if (!validate()) return;
    
    const n1 = Number(num1);
    const n2 = Number(num2);
    let res = 0;
    
    switch (operator) {
      case '+': res = n1 + n2; break;
      case '-': res = n1 - n2; break;
      case '*': res = n1 * n2; break;
      case '/': 
        if (n2 === 0) {
          setError('Không thể chia cho 0.');
          return;
        }
        res = n1 / n2; 
        break;
      default: return;
    }
    
    // Format to avoid long decimals
    setResult(`${n1} ${operator} ${n2} = ${Math.round(res * 1000000) / 1000000}`);
  };

  const reset = () => {
    setNum1('');
    setNum2('');
    setResult(null);
    setError('');
    num1Ref.current?.focus();
  };

  return (
    <div className="component-card glass-panel fade-in">
      <h2>Bảng tính</h2>
      
      {error && <div className="alert error">{error}</div>}
      
      <div className="form-group grid-2">
        <div>
          <label>Số thứ nhất (*)</label>
          <input 
            ref={num1Ref} 
            value={num1} 
            onChange={e => setNum1(e.target.value)} 
            type="text" 
            placeholder="Nhập số..." 
            className={error && isNaN(Number(num1)) && num1 !== '' ? 'invalid' : ''}
          />
        </div>
        <div>
          <label>Số thứ hai (*)</label>
          <input 
            value={num2} 
            onChange={e => setNum2(e.target.value)} 
            type="text" 
            placeholder="Nhập số..."
            className={error && isNaN(Number(num2)) && num2 !== '' ? 'invalid' : ''}
          />
        </div>
      </div>
      
      <div className="op-buttons">
        <button className="btn op-btn" onClick={() => calculate('+')}>Cộng (+)</button>
        <button className="btn op-btn" onClick={() => calculate('-')}>Trừ (-)</button>
        <button className="btn op-btn" onClick={() => calculate('*')}>Nhân (*)</button>
        <button className="btn op-btn" onClick={() => calculate('/')}>Chia (/)</button>
      </div>
      
      <div className="action-buttons mt-2">
        <button className="btn secondary block" onClick={reset}>Reset Bảng Tính</button>
      </div>
      
      {result !== null && (
        <div className="result-panel box-up">
          <h3>Kết quả:</h3>
          <p className="result-text">{result}</p>
        </div>
      )}
    </div>
  );
}

function App() {
  const [view, setView] = useState('equation'); // 'equation' | 'calculator'

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>Toán Học <span className="highlight">Pro</span></h1>
        <p className="subtitle">Công cụ giải phương trình và tính toán thông minh</p>
      </header>
      
      <main className="main-content">
        <div className="tabs-container glass-panel">
          <button 
            className={`tab-btn ${view === 'equation' ? 'active' : ''}`} 
            onClick={() => setView('equation')}
          >
            <span className="icon">📐</span>
            Giải Phương Trình Bậc Nhất
          </button>
          <button 
            className={`tab-btn ${view === 'calculator' ? 'active' : ''}`} 
            onClick={() => setView('calculator')}
          >
            <span className="icon">🧮</span>
            Bảng Tính (Máy Tính)
          </button>
        </div>

        <div className="view-container">
          {view === 'equation' ? <EquationSolver /> : <Calculator />}
        </div>
      </main>
    </div>
  );
}

export default App;
