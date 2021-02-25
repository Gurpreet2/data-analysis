import React, { Component } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import classes from './LogisticAnalysisScreen.module.css';

class LogisticAnalysisScreen extends Component {
  constructor(props) {
    super(props);
    this.state = {
      canvas: null,
      ctx: null,
      isDrawing: false,
      xOffset: 0,
      yOffset: 0,
      canvasWidth: 0,
      canvasHeight: 0,
      x: null,
      y: null,
      computersGuess: null,
    };
  }

  componentDidMount() {
    const canvas = document.getElementById("canvas-guessnumber");
    const canvasOffsets = canvas.getBoundingClientRect();
    const ctx = canvas.getContext("2d");
    ctx.lineCap = 'round';
    this.setState({
      canvas: canvas,
      ctx: ctx,
      xOffset: canvasOffsets.left,
      yOffset: canvasOffsets.top,
      canvasWidth: canvasOffsets.right - canvasOffsets.left,
      canvasHeight: canvasOffsets.bottom - canvasOffsets.top,
      imageData: null,
    });
  }

  mouseDownHandler = event => {
    this.setState({
      x: event.pageX,
      y: event.pageY,
      isDrawing: true,
    });
  }

  mouseMoveHandler = event => {
    if (this.state.isDrawing === true) {
      this.draw(event.pageX, event.pageY);
      this.setState({
        x: event.pageX,
        y: event.pageY,
      });
    }
  }

  mouseUpHandler = event => {
    if (this.state.isDrawing === true) {
      this.draw(event.pageX, event.pageY);
      this.setState({
        x: 0,
        y: 0,
        isDrawing: false,
      });
    }
  }

  mouseOverHandler = event => {
    if (event.buttons !== 1) {
      this.setState({
        x: 0,
        y: 0,
        isDrawing: false,
      });
    } else {
      this.setState({
        x: event.pageX,
        y: event.pageY,
        isDrawing: true,
      });
    }
  }

  draw = (newX, newY) => {
    const { ctx, x, y, xOffset, yOffset } = this.state;
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 20;
    ctx.moveTo(x - xOffset, y - yOffset);
    ctx.lineTo(newX - xOffset, newY - yOffset);
    ctx.stroke();
    ctx.closePath();
  }

  clearCanvasHandler = event => {
    this.state.ctx.clearRect(0, 0, this.state.canvasWidth, this.state.canvasHeight);
  }

  checkNumberHandler = event => {
    const resultArray = this.imageDataToMnistArray(this.state.ctx.getImageData(0, 0, this.state.canvasWidth, this.state.canvasHeight).data);
    fetch('http://localhost:5000/numbergame', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      referrerPolicy: 'no-referrer',
      body: JSON.stringify({
        transformed_array: resultArray
      })
    })
      .then(res => res.json())
      .then(result => this.setState({computersGuess: result.guess}))
      .catch(console.error);
  }

  train = num => {
    const resultArray = this.imageDataToMnistArray(this.state.ctx.getImageData(0, 0, this.state.canvasWidth, this.state.canvasHeight).data);
    fetch('http://localhost:5000/numbergame/train', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      referrerPolicy: 'no-referrer',
      body: JSON.stringify({
        transformed_array: resultArray,
        y_value: num,
      })
    })
      .catch(console.error);
  }

  imageDataToMnistArray = imageDataArray => {
    // convert to grayscale
    const grayScaleArray = this.convertToGrayscale(imageDataArray);
    // convert to multiarray
    const grayScaleMultiArray = this.convertTo2DArray(grayScaleArray, this.state.canvasWidth);
    // shrink to mnist size (28x28)
    const shrunkGrayScaleArray = this.shrink2DArray(grayScaleMultiArray);
    return shrunkGrayScaleArray;
  }

  /**
   * Convert an ImageData array ([r, b, g, a, r, b, g, a, ...]) to a grayscale ([gray, gray, ...])
   * Reduces length by 75%
   */
  convertToGrayscale = imageDataArray => {
    const grayScaleArray = [];
    for (let i = 0; i < imageDataArray.length; i+=4) {
      grayScaleArray.push((imageDataArray[i] + imageDataArray[i+1] + imageDataArray[i+2])/3);
    }
    return grayScaleArray;
  }

  convertTo2DArray = (oneDArray, width) => {
    const twoDArray = [];
    for (let i = 0; i < oneDArray.length; i+=width) {
      twoDArray.push(oneDArray.slice(i, i+width));
    }
    return twoDArray;
  }

  shrink2DArray = unshrunkArray => {
    const shrunkArray = [];
    for (let i = 0; i < 28; i+=1) {
      for (let j = 0; j < 28; j+=1) {
        let count = 0;
        for (let curI = 0; curI < this.state.canvasWidth/28; curI++) {
          for (let curJ = 0; curJ < this.state.canvasHeight/28; curJ++) {
            count += unshrunkArray[i*this.state.canvasWidth/28 + curI][j*this.state.canvasHeight/28 + curJ];
          }
        }
        shrunkArray.push(count/(this.state.canvasWidth/28*this.state.canvasHeight/28));
      }
    }
    return shrunkArray;
  }

  render() {
    return (
      <Container className="mt-4">
        <h1>The, Let The Computer Guess What Number You Drew, Game</h1>
        <Row>
          <canvas
            id="canvas-guessnumber"
            className={classes.Canvas}
            width="280"
            height="280"
            onMouseDown={this.mouseDownHandler}
            onMouseMove={this.mouseMoveHandler}
            onMouseUp={this.mouseUpHandler}
            onMouseOver={this.mouseOverHandler}
          />
          <div className="ml-5">
            <div>
              <Row>
                <Button variant="light" className="btn-outline-success" onClick={this.checkNumberHandler}>Check number</Button>
              </Row>
              <Row>
                <Button variant="light" className="mt-4 btn-outline-dark" onClick={this.clearCanvasHandler}>Clear</Button>
              </Row>
            </div>
            <ComputerGuess computersGuess={this.state.computersGuess} train={this.train} />
          </div>
        </Row>
      </Container>
    );
  }
}

const ComputerGuess = ({ computersGuess, train }) => {
  if (computersGuess !== null) {
    const nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    return (
      <>
        <div className="mt-5">
          The computer guessed {computersGuess}!
        </div>
        <div className="mt-2">
          <div className="mb-2">
            If that was not correct, please select the correct number from below:
          </div>
          <Row>
            {nums.map(num => <Col key={num} onClick={() => train(num)} style={{border: "1px solid black"}}>{num}</Col>)}
          </Row>
        </div>
      </>
    );
  } else {
    return null;
  }
}

export default LogisticAnalysisScreen;