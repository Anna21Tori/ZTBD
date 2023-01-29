import React, {useEffect, useState} from 'react';
import './App.css';
import {BasicTabs} from './tab/BasicPanel'
import Progress from './helper/Progress';
import Error from './helper/Error';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);


  return (
    <>
    <nav className="navbar navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">
        DB Performance
      </a>
      </div>
      
    </nav>
    <div style={{height:"5px"}}>
      {loading ? <Progress/> : ''}
    </div>
    
    <div className="container-fluid">
      <div className="row">
        <div className="col-8 offset-2">
           <BasicTabs setLoading={setLoading} setError={setError}/>
        </div>
      </div>
    </div>
    <Error setError={setError} error={error}/>
    </>
    
  );
}

export default App;
