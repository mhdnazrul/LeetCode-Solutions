class Solution {
public:
    string largestEven(string s) {
        int pos = -1;
        for (int i = s.size() - 1; i >= 0; i--) {
            if ((s[i] - '0') % 2 == 0) {
                pos = i;
                break;
            }
        }
        if (pos == -1) return "";
        string ans = "";
        for (int i = 0; i < s.size(); i++) {
            if (i <= pos) ans += s[i];
        }
        return ans;
    }
};