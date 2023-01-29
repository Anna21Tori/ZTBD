import React, {useEffect, useState} from 'react';
import { LineChart } from '../charts/LineChart';
import {TestPanelProps, TestResults} from "../interfaces/Interfaces";

export const TestPanel = (props: TestPanelProps) => {
    const { children, url, setLoading, setError, ... other } = props;
    const [test, setTest] = useState<TestResults>({});


    useEffect(() => {
    fetch(`http://localhost:8000${url}`)
    .then((response) => {
      if (!response.ok) {
        setError(true);
        setTest({});
      }
      return response.json();
    }).then((actualData: TestResults) => {
        const results: TestResults = {
          ... actualData
        }
        setTest(results);
        setError(false);
        console.log(results)
      })
      .catch(() => {
        setError(true);
        setTest({});
      })
      .finally(() => {
        setLoading(false);
      });
    }, []);

    const labels = test != null && test.mongodb != null ? test.mongodb.test.map(item => item.num_records.toString()) : [];
    const mongo = test != null && test.mongodb != null ? test.mongodb.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];
    const postgresql = test != null && test.postgresql != null ? test.postgresql.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];
    const redis = test != null && test.redis != null ? test.redis.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];

    return <LineChart labels={labels} mongo={mongo} postgre={postgresql} redis={redis}/>
}