// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/utils/math/Math.sol";
import "@openzeppelin/contracts/utils/Strings.sol"; 
import "forge-std/Test.sol";

contract Grading is Test{
	uint256 public score;
	uint256 public maxScore;
	string public scoreFile = "score.txt";

	function setMaxScore(uint256 _maxScore ) internal {
		maxScore = _maxScore;
	}

	function setScoreFile(string memory _scoreFile) internal {
		scoreFile = _scoreFile;
	}
	
	function scoreEq( uint256 a, uint256 b ) internal {
		if( a == b ) {
			score++;
			vm.writeFile( scoreFile, Strings.toString(score) );
		}
	}

	function scoreLT( uint256 a, uint256 b ) internal {
		if( a < b ) {
			score++;
			vm.writeFile( scoreFile, Strings.toString(score) );
		}
	}

	function scoreGT( uint256 a, uint256 b ) internal {
		if( a > b ) {
			score++;
			vm.writeFile( scoreFile, Strings.toString(score) );
		}
	}
}
