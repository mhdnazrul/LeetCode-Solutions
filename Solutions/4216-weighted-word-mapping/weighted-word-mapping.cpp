class Solution {
public:
    string mapWordWeights(vector<string>& words, vector<int>& weights) {
        string ans;
        for (string s : words) {
            int cnt = 0;
            for (int i = 0; i < s.size(); i++) {
                cnt += weights[(s[i] - 'a')];
            }
            ans += ('a' + (25 - (cnt % 26)));
        }
        return ans;
    }
};