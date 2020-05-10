import React, { useState, useEffect } from 'react';
import logo from '../assets/logo.png';
import { API_BASE_URL } from '../config';
import { Link } from 'react-router-dom';
function App() {
  const [walletInfo, setWalletInfo] = useState({});
  const { address, balance } = walletInfo;
  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then((response) => response.json())
      .then((json) => setWalletInfo(json));
  }, []);

  return (
    <div className="App">
      <img className="logo" src={logo} alt="app-logo" />
      <h3>Welcome to Python Blockchain</h3>
      <br />
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/conduct-transaction">Conduct a transaction</Link>
      <Link to="/transaction-pool">Transaction Pool</Link>

      <br />
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
    </div>
  );
}

export default App;
