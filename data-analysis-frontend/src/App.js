import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Jumbotron } from 'react-bootstrap';
import './App.css';
import Header from './components/Header/Header';
import LinearAnalysisScreen from './components/LinearAnalysis/LinearAnalysisScreen';
import LogisticAnalysisScreen from './components/LogisticAnalysis/LogisticAnalysisScreen';


class App extends Component {
  render() {
    return (
      <Router>
        <Header />
        <Route exact path="/" render={(props) => (
          <Jumbotron className="container mt-5 pb-5">
            <h1>Welcome to the Data Analysis Platform!</h1>
            <p>Next up, convert files into datasets, and store them in a database. Next, do something with logarithmic regression related to finance</p>
          </Jumbotron>
        )} />
        <Route path="/linear" component={LinearAnalysisScreen} />
        <Route path="/logistic" component={LogisticAnalysisScreen} />
      </Router>
    );
  }
}

export default App;