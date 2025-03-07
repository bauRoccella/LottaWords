import React from 'react';
import styled from 'styled-components';

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1a1a1a;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;
`;

const NavLink = styled.a`
  color: white;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s ease;
  
  &:hover {
    color: #ff5a57;
  }
`;

const Navbar: React.FC = () => {
  return (
    <Nav>
      <Logo>LottaWords</Logo>
      <NavLinks>
        <NavLink href="https://www.nytimes.com/puzzles/letter-boxed" target="_blank" rel="noopener noreferrer">NYT Letter Boxed</NavLink>
        <NavLink href="https://github.com/bauRoccella/LottaWords" target="_blank" rel="noopener noreferrer">GitHub Repo</NavLink>
        <NavLink href="https://www.linkedin.com/in/bautistaroccella/" target="_blank" rel="noopener noreferrer">LinkedIn</NavLink>
      </NavLinks>
    </Nav>
  );
};

export default Navbar;
