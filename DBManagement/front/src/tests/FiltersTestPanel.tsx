import React, {useEffect, useState} from 'react';
import { BarChart } from '../charts/BarChart';
import {TestPanelProps, TestFiltersResults} from "../interfaces/Interfaces"
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
export const FiltersTestPanel = (props: TestPanelProps) => {
    const { children, url, setLoading, setError, ... other } = props;
    const [test, setTest] = useState<TestFiltersResults>({sqls:[]});
    const [page, setPage] = React.useState(1);


    useEffect(() => {
    fetch(`http://localhost:8000${url}`)
    .then((response) => {
      if (!response.ok) {
        setError(true);
        setTest({sqls:[]});
      }
      return response.json();
    }).then((actualData: TestFiltersResults) => {
        const results: TestFiltersResults = {
          ... actualData
        }
        setTest(results);
        setError(false);
        console.log(results)
      })
      .catch(() => {
        setError(true);
        setTest({sqls:[]});
      })
      .finally(() => {
        setLoading(false);
      });
    }, []);

    const labels = test != null && test.mongodb != null ? test.mongodb.test.map(item => item.num_records.toString()) : [];
    const mongo = test != null && test.mongodb != null ? test.mongodb.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];
    const postgresql = test != null && test.postgresql != null ? test.postgresql.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];
    const redis = test != null && test.redis != null ? test.redis.test.map(item => item.time.reduce((a, b) => a + b, 0)/item.time.length) : [];

    
    const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
    };

    return <>
        
        
        <BarChart labels={[labels[page-1]]} mongo={[mongo[page-1]]} postgre={[postgresql[page-1]]} redis={[redis[page-1]]}/>
         <div style={{height:"6rem"}}>
            <p>{test != null ? test.sqls[page-1]: ''}</p>
        </div>
        <div className='d-flex justify-content-center'>
            <Stack spacing={test.sqls.length}>
                <Pagination count={test.sqls.length} variant="outlined" color="secondary" page={page} onChange={handleChange}/>
            </Stack>
        </div>
         
    </> 

}