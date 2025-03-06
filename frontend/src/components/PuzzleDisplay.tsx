import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  gap: 2rem;
`;

const PuzzleBox = styled.div`
  background-color: #2a2a2a;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
`;

const Title = styled.h2`
  color: white;
  text-align: center;
  margin-bottom: 1.5rem;
`;

const LetterGrid = styled.div`
  display: grid;
  grid-template-rows: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
`;

const SideContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
`;

const Letter = styled.div`
  background-color: #faa6a4;
  color: white;
  padding: 1rem;
  border-radius: 5px;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  transition: transform 0.2s ease;
  min-width: 3rem;
  
  &:hover {
    transform: scale(1.05);
  }
`;

const SolutionSection = styled.div`
  background-color: #333;
  padding: 1rem;
  border-radius: 5px;
  margin-top: 1rem;
`;

const SolutionTitle = styled.h3`
  color: white;
  margin-bottom: 1rem;
`;

const SolutionList = styled.ul`
  list-style: none;
  padding: 0;
  color: white;
`;

const SolutionItem = styled.li`
  padding: 0.5rem;
  border-bottom: 1px solid #444;
  
  &:last-child {
    border-bottom: none;
  }
`;

interface PuzzleData {
  square: {
    top: string;
    right: string;
    bottom: string;
    left: string;
  };
  nyt_solution: string[];
  lotta_solution: string[];
  error: string | null;
}

const PuzzleDisplay: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [puzzleData, setPuzzleData] = useState<PuzzleData>({
    square: {
      top: '',
      right: '',
      bottom: '',
      left: ''
    },
    nyt_solution: [],
    lotta_solution: [],
    error: null
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPuzzleData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/puzzle');
        const data = await response.json();
        console.log('API Response:', data);
        setPuzzleData(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching puzzle data:', error);
        setError('Failed to fetch puzzle data');
        setIsLoading(false);
      }
    };

    fetchPuzzleData();
  }, []);

  if (isLoading) {
    return <Container>Loading puzzle...</Container>;
  }

  if (error || !puzzleData) {
    return <Container>Error: {error || 'Failed to load puzzle data'}</Container>;
  }

  return (
    <Container>
      <PuzzleBox>
        <Title>Today's Puzzle</Title>
        <LetterGrid>
          {/* Top side */}
          <SideContainer>
            {puzzleData?.square?.top ? puzzleData.square.top.split('').map((letter: string, index: number) => (
              <Letter key={`top-${index}`}>{letter}</Letter>
            )) : <div>No data available</div>}
          </SideContainer>
          
          {/* Middle row with left and right sides */}
          <SideContainer>
            {puzzleData?.square?.left?.split('').map((letter: string, index: number) => (
              <Letter key={`left-${index}`}>{letter}</Letter>
            ))}
            <div style={{ flex: 1 }} /> {/* Spacer */}
            {puzzleData?.square?.right?.split('').map((letter: string, index: number) => (
              <Letter key={`right-${index}`}>{letter}</Letter>
            ))}
          </SideContainer>
          
          {/* Bottom side */}
          <SideContainer>
            {puzzleData?.square?.bottom?.split('').map((letter: string, index: number) => (
              <Letter key={`bottom-${index}`}>{letter}</Letter>
            ))}
          </SideContainer>
        </LetterGrid>

        <SolutionSection>
          <SolutionTitle>NYT Solution</SolutionTitle>
          <SolutionList>
            {puzzleData.nyt_solution.map((solution: string, index: number) => (
              <SolutionItem key={`nyt-${index}`}>{solution}</SolutionItem>
            ))}
          </SolutionList>
        </SolutionSection>

        <SolutionSection>
          <SolutionTitle>LottaWords Solution</SolutionTitle>
          <SolutionList>
            {puzzleData.lotta_solution.map((solution: string, index: number) => (
              <SolutionItem key={`lotta-${index}`}>{solution}</SolutionItem>
            ))}
          </SolutionList>
        </SolutionSection>
      </PuzzleBox>
    </Container>
  );
};

export default PuzzleDisplay;