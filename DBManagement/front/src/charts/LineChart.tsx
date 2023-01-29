import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2'
import { LineChartProps } from '../interfaces/Interfaces';


ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'right' as const,
    },
    title: {
      display: false,
      text: '',
    },
  },
  scales: {
      y: {
        title: {
          display: true,
          text: 'Times'
        },
        ticks: {
          callback: function(val: number | string, index: any) {
            // Hide every 2nd tick label
            return `${val} ms`;
          }
        }
      },
      x: {
        title: {
          display: true,
          text: 'Records'
        },
      }
    },
};




export const LineChart = (props: LineChartProps) =>{
  const {children, labels, mongo, postgre, redis, ... other} = props;
  const data = {
  labels,
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
            <Line options={options} data={data} height={100}/>
        </div>;
}