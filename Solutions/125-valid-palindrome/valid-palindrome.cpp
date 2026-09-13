class Solution {
public:
    bool isPalindrome(string s) {
        string t;

        for (char c : s) {
            if (isalnum(c))
                t += tolower(c);
        }

        string rev = t;
        reverse(rev.begin(), rev.end());

        return t == rev;
    }
};