import React, { useState, useEffect, useRef } from 'react';
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

const PuzzleGridContainer = styled.div`
  position: relative;
  width: 300px;
  height: 300px;
  margin-bottom: 2rem;
  margin-left: auto;
  margin-right: auto;
`;

const ConnectionsOverlay = styled.svg`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
`;

const Square = styled.rect`
  fill: none;
  stroke: white;
  stroke-width: 2;
`;

const LetterPosition = styled.div`
  position: absolute;
  z-index: 2;
`;

const SideContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
`;

const Letter = styled.div`
  background-color: #faa6a4;
  color: white;
  padding: 0.8rem;
  border-radius: 5px;
  text-align: center;
  font-size: 1.3rem;
  font-weight: bold;
  transition: transform 0.2s ease;
  min-width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
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
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const [letterPositions, setLetterPositions] = useState<{[key: string]: {x: number, y: number}}>({});

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

  useEffect(() => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      setContainerSize({ width, height });
    }
  }, [puzzleData]);

  const calculateLetterPositions = () => {
    const positions: {[key: string]: {x: number, y: number}} = {};
    const padding = 35;
    const width = containerSize.width - 2 * padding;
    const height = containerSize.height - 2 * padding;
    
    if (puzzleData.square.top) {
      const topLetters = puzzleData.square.top.split('');
      const letterWidth = width / topLetters.length;
      topLetters.forEach((letter, index) => {
        positions[`top-${index}`] = {
          x: padding + letterWidth * index + letterWidth / 2,
          y: padding
        };
      });
    }
    
    if (puzzleData.square.right) {
      const rightLetters = puzzleData.square.right.split('');
      const letterHeight = height / rightLetters.length;
      rightLetters.forEach((letter, index) => {
        positions[`right-${index}`] = {
          x: width + padding,
          y: padding + letterHeight * index + letterHeight / 2
        };
      });
    }
    
    if (puzzleData.square.bottom) {
      const bottomLetters = puzzleData.square.bottom.split('');
      const letterWidth = width / bottomLetters.length;
      bottomLetters.forEach((letter, index) => {
        positions[`bottom-${index}`] = {
          x: padding + letterWidth * index + letterWidth / 2,
          y: height + padding
        };
      });
    }
    
    if (puzzleData.square.left) {
      const leftLetters = puzzleData.square.left.split('');
      const letterHeight = height / leftLetters.length;
      leftLetters.forEach((letter, index) => {
        positions[`left-${index}`] = {
          x: padding,
          y: padding + letterHeight * index + letterHeight / 2
        };
      });
    }
    
    setLetterPositions(positions);
  };
  
  useEffect(() => {
    if (containerSize.width > 0 && containerSize.height > 0) {
      calculateLetterPositions();
    }
  }, [containerSize, puzzleData]);

  const generateConnections = () => {
    if (!puzzleData || !puzzleData.lotta_solution || !puzzleData.lotta_solution.length) {
      return null;
    }
    
    const solution = puzzleData.lotta_solution;
    const paths = [];
    
    for (let wordIndex = 0; wordIndex < solution.length; wordIndex++) {
      const word = solution[wordIndex];
      
      for (let i = 0; i < word.length - 1; i++) {
        const startLetter = word[i];
        const endLetter = word[i + 1];
        
        const startPos = findLetterPosition(startLetter);
        const endPos = findLetterPosition(endLetter);
        
        if (startPos && endPos) {
          paths.push(
            <path 
              key={`path-${wordIndex}-${i}`}
              d={`M ${startPos.x} ${startPos.y} L ${endPos.x} ${endPos.y}`}
              stroke="#faa6a4"
              strokeWidth="2"
              strokeOpacity="0.6"
              strokeDasharray="5,5"
              fill="none"
            />
          );
        }
      }
    }
    
    return paths;
  };
  
  const findLetterPosition = (letter: string) => {
    const sides = ['top', 'right', 'bottom', 'left'];
    
    for (const side of sides) {
      const letters = puzzleData.square[side as keyof typeof puzzleData.square].split('');
      const index = letters.findIndex(l => l.toUpperCase() === letter.toUpperCase());
      
      if (index !== -1) {
        return letterPositions[`${side}-${index}`];
      }
    }
    
    return null;
  };

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
        
        <PuzzleGridContainer ref={containerRef}>
          {containerSize.width > 0 && (
            <ConnectionsOverlay>
              <Square 
                x={35} 
                y={35} 
                width={containerSize.width - 70} 
                height={containerSize.height - 70} 
              />
              {generateConnections()}
            </ConnectionsOverlay>
          )}
          
          {/* Top side */}
          {puzzleData?.square?.top && puzzleData.square.top.split('').map((letter, index) => (
            <LetterPosition 
              key={`top-${index}`}
              style={{
                top: letterPositions[`top-${index}`]?.y - 20 || 0,
                left: letterPositions[`top-${index}`]?.x - 20 || 0,
              }}
            >
              <Letter>{letter}</Letter>
            </LetterPosition>
          ))}
          
          {/* Right side */}
          {puzzleData?.square?.right && puzzleData.square.right.split('').map((letter, index) => (
            <LetterPosition 
              key={`right-${index}`}
              style={{
                top: letterPositions[`right-${index}`]?.y - 20 || 0,
                left: letterPositions[`right-${index}`]?.x - 20 || 0,
              }}
            >
              <Letter>{letter}</Letter>
            </LetterPosition>
          ))}
          
          {/* Bottom side */}
          {puzzleData?.square?.bottom && puzzleData.square.bottom.split('').map((letter, index) => (
            <LetterPosition 
              key={`bottom-${index}`}
              style={{
                top: letterPositions[`bottom-${index}`]?.y - 20 || 0,
                left: letterPositions[`bottom-${index}`]?.x - 20 || 0,
              }}
            >
              <Letter>{letter}</Letter>
            </LetterPosition>
          ))}
          
          {/* Left side */}
          {puzzleData?.square?.left && puzzleData.square.left.split('').map((letter, index) => (
            <LetterPosition 
              key={`left-${index}`}
              style={{
                top: letterPositions[`left-${index}`]?.y - 20 || 0,
                left: letterPositions[`left-${index}`]?.x - 20 || 0,
              }}
            >
              <Letter>{letter}</Letter>
            </LetterPosition>
          ))}
        </PuzzleGridContainer>

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