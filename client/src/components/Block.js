import React, { useState } from 'react';
import { MILLISECONDS_PY } from '../config';
import Transaction from './Transaction';
import { Button } from 'react-bootstrap';

function ToggleTransactionDisplay({ block }) {
  const [displayTransaction, setDisplayTransaction] = useState(false);
  const { data } = block;

  const toggleTransactionDisplay = () => {
    setDisplayTransaction(!displayTransaction);
  };
  if (displayTransaction) {
    return (
      <div>
        {data.map((transaction) => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
        <br />
        <Button variant="danger" size="sm" onClick={toggleTransactionDisplay}>
          Show Less
        </Button>
      </div>
    );
  }
  if (data.length > 0) {
    return (
      <div>
        <br />

        <Button variant="danger" size="sm" onClick={toggleTransactionDisplay}>
          Show More
        </Button>
      </div>
    );
  }
  return <div>There is no block</div>;
}

export default function Block({ block }) {
  const { timestamp, hash } = block;
  const hashDisplay = `${hash.substring(0, 15)}...`;
  const timestampDisplay = new Date(
    timestamp / MILLISECONDS_PY
  ).toLocaleString();

  return (
    <div className="Block">
      <div>Hash: {hashDisplay}</div>
      <div>Timestamp: {timestampDisplay}</div>
      <ToggleTransactionDisplay block={block} />
    </div>
  );
}
