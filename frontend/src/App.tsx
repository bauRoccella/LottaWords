import React from 'react';
import styled from 'styled-components';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import PuzzleDisplay from './components/PuzzleDisplay';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #121212;
  color: white;
`;

const MainContent = styled.main`
  padding: 2rem;
  padding-bottom: 6rem; // Space for footer
`;

const App: React.FC = () => {
  return (
    <AppContainer>
      <Navbar />
      <MainContent>
        <PuzzleDisplay />
      </MainContent>
      <Footer />
    </AppContainer>
  );
};

export default App;
