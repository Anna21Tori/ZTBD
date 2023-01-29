export interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

export interface BasicPanelProps {
  children?: React.ReactNode;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setError: React.Dispatch<React.SetStateAction<boolean>>;
}
export interface TestFiltersResults {
    mongodb?: TestItem;
    postgresql?: TestItem;
    redis?: TestItem;
    sqls: string[]
}

export interface TestResults {
    mongodb?: TestItem;
    postgresql?: TestItem;
    redis?: TestItem
}

export interface TestItem {
  test: {
    num_records: number;
    time: number[];
  }[] 
}

export interface TestPanelProps {
    children?: React.ReactNode;
    setLoading: React.Dispatch<React.SetStateAction<boolean>>;
    setError: React.Dispatch<React.SetStateAction<boolean>>;
    url: string
}

export interface ErrorProps {
    children?: React.ReactNode;
    setError: React.Dispatch<React.SetStateAction<boolean>>;
    error: boolean;
    
}

export interface LineChartProps{
  children?: React.ReactNode;
  labels: string[],
  mongo: number[],
  postgre: number[],
  redis: number[]
}