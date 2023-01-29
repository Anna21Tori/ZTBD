import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { TestPanel } from '../tests/TestPanel';
import TabPanel from './TabPanel';
import {BasicPanelProps} from "../interfaces/Interfaces"
import { FiltersTestPanel } from '../tests/FiltersTestPanel';

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export function BasicTabs(props: BasicPanelProps) {
  const { children, setLoading, setError, ...other } = props;
  const [value, setValue] = React.useState(0);
  const urls = ["/test/insert", "/test/delete"]

  const panels = urls.map((url, i)=> {
    
    return <TabPanel value={value} index={i} key={i}>
        <TestPanel url={url} setLoading={setLoading} setError={setError}/>
      </TabPanel>
  })
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%', height:"80%" }} >
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
          <Tab label="Insert" {...a11yProps(0)} />
          <Tab label="Delete" {...a11yProps(1)} />
          <Tab label="Filters" {...a11yProps(2)} />
        </Tabs>
      </Box>
      {panels}
      <TabPanel value={value} index={2}>
        <FiltersTestPanel url={"/test/filters"} setLoading={setLoading} setError={setError}/>
      </TabPanel>
    </Box>
  );
}