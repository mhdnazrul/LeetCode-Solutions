class Solution {
public:
    bool isPalindrome(int x) {
        string nums = to_string(x);
        reverse(nums.begin(), nums.end());
        string n = to_string(x);
        if(n==nums)return true;
        else return false;
    }
};