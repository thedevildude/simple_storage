// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    
    // this will get initialized to 0
    uint256 FavouriteNumber;
    
    struct People {
        uint256 FavouriteNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nametoFavouriteNumber;
    
    
    function store(uint256 _favouriteNumber) public returns(uint256) {
        FavouriteNumber = _favouriteNumber;
        return _favouriteNumber;
    }
    
    //view, pure
    function retrieve() public view returns(uint256) {
        return FavouriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber, _name));
        nametoFavouriteNumber[_name] = _favouriteNumber;
    }
}