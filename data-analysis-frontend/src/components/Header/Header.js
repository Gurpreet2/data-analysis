import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

const Header = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <div className="container">
        <Navbar.Brand href="/">Data Analysis</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="/linear">Linear Analysis</Nav.Link>
          <Nav.Link href="/logistic">Logistic Analysis</Nav.Link>
        </Nav>
      </div>
    </Navbar>
  );
}

export default Header;