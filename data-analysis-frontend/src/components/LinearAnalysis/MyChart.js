import React, { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Chart from 'chart.js';
import classes from './MyChart.module.css';

const MyChart = ({ field_metadata, setXField, setYField, setFrequency, getData, scatterData, xField, lin_reg_data }) => {
  const [chart, setChart] = useState(null);
  const fields = Object.keys(field_metadata);
  let xAxesOptions;
  if (field_metadata[xField] === 'date') {
    xAxesOptions = {
      type: 'time',
      time: { parser: 'YYYY-MM-DDHH:mm:ss'}
    };
  } else {
    xAxesOptions = {};
  }

  useEffect(() => {
    const ctx = document.getElementById('myChart').getContext('2d');
    setChart(new Chart(ctx, {
      // The type of chart we want to create
      type: 'scatter',
      // The data for our dataset
      data: {
          datasets: [
            {
              label: 'My dataset',
              backgroundColor: 'green',
              borderColor: 'orange',
              data: []
            },
          ]
      },
      // Configuration options go here
      options: {
        scales: {
          xAxes: [{}]
        }
      }
    }));
  }, []);

  useEffect(() => {
    if (chart !== null) {
      chart.data.datasets[0].data = scatterData;
      if (lin_reg_data.length > 0) {
        if (chart.data.datasets.length <= 1) {
          chart.data.datasets.push({
            label: 'Best fit line',
            borderColor: 'red',
            data: lin_reg_data,
            type: 'line',
            fill: false,
          });
        } else {
          chart.data.datasets[1].data = lin_reg_data;
        }
      }
      chart.options.scales.xAxes = [xAxesOptions];
      chart.update();
    }
  }, [chart, xAxesOptions, scatterData, lin_reg_data]);

  return (
    <>
      <Form className="mt-4 mb-4">
        <Form.Group className="form-group">
          <Form.Label htmlFor="x-select">Choose an X:</Form.Label>
          <Form.Control as="select" size="sm" name="xField" id="x-select" onChange={setXField}>
            <option key="xSelectDefault" value="">Please select a field</option>
            {fields.map(field => <option key={field} value={field}>{field}</option>)}
          </Form.Control>
        </Form.Group>
      </Form>
      <Form className="mt-4 mb-4">
        <Form.Group className="form-group">
          <Form.Label htmlFor="y-select">Choose a Y:</Form.Label>
          <Form.Control as="select" size="sm" name="yField" id="y-select" onChange={setYField}>
            <option key="ySelectDefault" value="">Please select a field</option>
            {fields.map(field => <option key={field} value={field}>{field}</option>)}
          </Form.Control>
        </Form.Group>
      </Form>
      <ChooseFrequency setFrequency={setFrequency} />
      <Button onClick={getData}>Click me to load chart</Button>
      <canvas id="myChart"></canvas>
    </>
  );
}

const ChooseFrequency = ({ setFrequency }) => {
  return (
    <div className={classes.RadioSelection}>
      <span className={classes.RadioSelectionSpan}>
        <input className={classes.RadioSelectionInput} type="radio" id="firstRadio" name="frequency" value="NONE" onClick={setFrequency} />
        <label htmlFor="firstRadio">None</label>
      </span>
      <span className={classes.RadioSelectionSpan}>
        <input className={classes.RadioSelectionInput} type="radio" id="secondRadio" name="frequency" value="DAILY" onClick={setFrequency} />
        <label htmlFor="secondRadio">Daily</label>
      </span>
      <span className={classes.RadioSelectionSpan}>
        <input className={classes.RadioSelectionInput} type="radio" id="thirdRadio" name="frequency" value="MONTHLY" onClick={setFrequency} />
        <label htmlFor="thirdRadio">Monthly</label>
      </span>
    </div>
  );
}

export default MyChart;