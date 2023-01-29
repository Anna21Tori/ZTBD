import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { LineChartProps } from '../interfaces/Interfaces';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  elements: {
    bar: {
      borderWidth: 2,
    },
  },
  responsive: true,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'right' as const,
    },
    title: {
      display: false,
    },
  },
};






export const BarChart = (props: LineChartProps) =>{
  const {children, labels, mongo, postgre, redis, ... other} = props;
  const data = {
    labels: labels,
  maintainAspectRatio: false,
  datasets: [
    {
      label: 'MongoDB',
      data: mongo,
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
    {
      label: 'PostgreSQL',
      data: postgre,
      borderColor: 'rgb(53, 162, 235)',
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    },
    {
      label: 'Redis',
      data: redis,
      borderColor: 'rgb(63, 84, 73)',
      backgroundColor: 'rgba(63, 84, 73, 0.5)',
    },
  ],
};
  return <div  className="d-flex justify-content-center">
            <Bar options={options} data={data} height={100}/>
        </div>;
}