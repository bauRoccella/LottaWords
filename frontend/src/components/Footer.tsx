import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  background-color: #1a1a1a;
  color: white;
  position: fixed;
  bottom: 0;
  width: 100%;
`;

const FooterContent = styled.div`
  text-align: center;
  font-size: 0.9rem;
`;

const Link = styled.a`
  color: #4a9eff;
  text-decoration: none;
  
  &:hover {
    text-decoration: underline;
  }
`;

const Footer: React.FC = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <p>
          Created by{' '}
          <Link href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer">
            Your Name
          </Link>{' '}
          © {new Date().getFullYear()}
        </p>
      </FooterContent>
    </FooterContainer>
  );
};

export default Footer;
