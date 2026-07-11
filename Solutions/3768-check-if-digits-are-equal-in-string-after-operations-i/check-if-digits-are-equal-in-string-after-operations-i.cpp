class Solution {
public:
    bool allSameDigits(const string& x) {
        return all_of(x.begin(), x.end(), [&](char c) { return c == x[0]; });
    }
    bool hasSameDigits(string s) {
        if (allSameDigits(s))
            return true;
        while (s.size() > 2) {
            string tp;
            for (int i = 1; i < (int)s.size(); i++) {
                tp += ((s[i - 1] - '0' + s[i] - '0') % 10) + '0';
            }
            s = tp;
        }
        return s[0] == s[1];
    }
};