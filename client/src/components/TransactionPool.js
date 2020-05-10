import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Transaction from './Transaction';
import { Button } from 'react-bootstrap';
import { API_BASE_URL, SECONDS_JS } from '../config';
import history from '../history';

const POLL_INTERVAL = SECONDS_JS * 10;
function TransactionPool() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = () => {
    fetch(`${API_BASE_URL}/transactions`)
      .then((response) => response.json())
      .then((json) => {
        console.log('transactions json', json);
        setTransactions(json);
      });
  };

  const fetchMineBlock = () => {
    fetch(`${API_BASE_URL}/blockchain/mine`).then(() => {
      alert('SUCCESS');
      history.push('/blockchain');
    });
  };

  useEffect(() => {
    fetchTransactions();
    // Updates transaction pool every 10 seconds.
    const intervalId = setInterval(fetchTransactions, POLL_INTERVAL);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="TransactionPool">
      <Link to="/">Home</Link>
      <br />
      <h3>Transaction Pool</h3>
      <div>
        {transactions.map((transaction) => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
      </div>
      <hr />
      <Button variant="danger" onClick={fetchMineBlock}>
        Mine a block of these transactions
      </Button>
    </div>
  );
}

export default TransactionPool;
