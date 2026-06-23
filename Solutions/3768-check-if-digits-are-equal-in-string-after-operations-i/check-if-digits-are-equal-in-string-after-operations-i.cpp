class Solution {
public:
    bool hasSameDigits(string s) {
        while(s.size()>2){
            string tp;
            for(int i=1; i<(int)s.size(); i++){
                tp+= ((s[i-1]-'0'+s[i]-'0')%10)+'0';
            }
            s=tp;
        }
        return s[0]==s[1];
    }
};