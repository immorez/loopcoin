import React, { useState, useEffect } from 'react';
import Block from './Block';
import { API_BASE_URL } from '../config';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
const PAGE_RANGE = 3;

export default function Blockchain() {
  const [blockchain, setBlockchain] = useState([]);
  const [blockchainLength, setBlockchainLength] = useState(0);

  const fetchBlockchainPage = ({ start, end }) => {
    fetch(
      `${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`
    ).then((response) => response.json().then((json) => setBlockchain(json)));
  };

  useEffect(() => {
    fetchBlockchainPage({ start: 0, end: PAGE_RANGE });
    fetch(`${API_BASE_URL}/blockchain`)
      .then((response) => response.json())
      .then((json) => setBlockchain(json));

    fetch(`${API_BASE_URL}/blockchain/length`)
      .then((response) => response.json())
      .then((json) => setBlockchainLength(json));
  }, []);

  const buttonNumbers = [];
  for (let i = 0; i < Math.ceil(blockchainLength / PAGE_RANGE); i++) {
    buttonNumbers.push(i);
  }

  return (
    <div className="Blockchain">
      <Link to="/">Home</Link>
      <h3>Blockchain</h3>
      <div>
        {blockchain.map((block) => (
          <Block key={block.hash} block={block} />
        ))}
      </div>
      <div>
        {buttonNumbers.map((number) => {
          const start = number * PAGE_RANGE;
          const end = (number + 1) * PAGE_RANGE;
          return (
            <span
              key={number}
              onClick={() => fetchBlockchainPage({ start, end })}
            >
              <Button variant="danger" size="sm">
                {number + 1}
              </Button>{' '}
            </span>
          );
        })}
      </div>
    </div>
  );
}
