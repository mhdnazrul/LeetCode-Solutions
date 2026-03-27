class Solution {
public:
    int reverse(int x) {
        string s = to_string(x);
        bool neg = false;
        if (s[0] == '-') {
            neg = true;
            s.erase(0, 1);
        }
        
        std::reverse(s.begin(), s.end());
        long long num = stoll(s);
        if (neg) num = -num;
        if (num > INT_MAX || num < INT_MIN) return 0;
        return (int)num;
    }
};