class Solution {
public:
    int lengthOfLastWord(string s) {
        int cur = 0, ans = 0;

        for (int i = 0; i < s.size(); i++) {
            char ch = s[i];

            if (ch != ' ') {
                cur++;
            } else {
                if (cur > 0) {
                    ans = cur;
                    cur = 0;
                }
            }
        }
        if (cur > 0)
            ans = cur;

        return ans;
    }
};