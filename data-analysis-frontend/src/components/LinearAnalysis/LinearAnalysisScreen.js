import React, { PureComponent } from 'react';
import Files from '../Files/Files';
import MyChart from './MyChart';

class LinearAnalysisScreen extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
      selectedFile: null,
      frequency: 'NONE',
      field_metadata: {},
      xField: null,
      yField: null,
      sortByX: true,
      scatterData: [],
      theta: [],
      lin_reg_data: [],
    };
  }

  componentDidMount() {
    this.getFiles();
  }

  /**
   * Retrieve list of files that can be analyzed. Sort the list by name, and put it in `this.state.files`.
   */
  getFiles = event => {
    fetch("http://localhost:5000/files")
      .then(res => res.json())
      .then(
        result => {
          const sortedResult = result.slice().sort((a, b) => a.name > b.name ? 1 : -1);
          this.setState({files: sortedResult});
        }
      )
      .catch(error => console.log(error));
  }

  /**
   * Choose a specific file for analysis. After a file is chosen, a call is made to fetch the fields contained in the file.
   */
  selectFile = event => {
    this.setState({selectedFile: event.target.value});
    fetch(`http://localhost:5000/field_metadata?file_id=${event.target.value}`)
      .then(res => res.json())
      .then(result => this.setState({field_metadata: result}))
      .catch(error => console.log(error));
  }

  /**
   * Fetch the data!
   */
  getData = event => {
    const params = [
      {param: 'file_id', value: this.state.selectedFile},
      {param: 'xField', value: this.state.xField},
      {param: 'yField', value: this.state.yField},
      {param: 'frequency', value: this.state.frequency},
      {param: 'sortByX', value: this.state.sortByX}
    ].map(item => item.param + '=' + item.value).join('&');
    fetch('http://localhost:5000/data?' + params)
      .then(res => res.json())
      .then(result => {
        this.setState({
          scatterData: [...result.x_values].map((item, idx) => { // assuming result[0] and result[1] are the same length...
            return {
              x: item,
              y: result.y_values[idx]
            };
          }),
          theta: result.theta,
          lin_reg_data: result.theta.length > 0 ? [...result.x_values].map((item, idx) => { // assuming result[0] and result[1] are the same length...
            return {
              x: item,
              y: result.lin_reg_y_values[idx],
            };
          }) : [],
        })
      })
      .catch(error => console.log(error));
  }

  /**
   * Select X field
   */
  setXField = event => this.setState({xField: event.target.value});

  /**
   * Select Y field
   */
  setYField = event => this.setState({yField: event.target.value});

  /**
   * Set chosen frequency
   * NONE means pull all data
   */
  setFrequency = event => this.setState({frequency: event.target.value});

  render() {
    return (
      <>
        <div className="container">
          <Files files={this.state.files} getFiles={this.getFiles} selectFile={this.selectFile} />
          <MyChart
            field_metadata={this.state.field_metadata} scatterData={this.state.scatterData} theta={this.state.theta} lin_reg_data={this.state.lin_reg_data}
            setXField={this.setXField} setYField={this.setYField} getData={this.getData} setFrequency={this.setFrequency} xField={this.state.xField}
          />
        </div>
      </>
    );
  }
}

export default LinearAnalysisScreen;