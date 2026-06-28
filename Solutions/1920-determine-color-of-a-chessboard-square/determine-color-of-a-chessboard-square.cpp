class Solution {
public:
    bool squareIsWhite(string coordinates) {
        int x = coordinates[0]-'0' - 48;
        int y = coordinates[1]-'0';
        if((x+y)%2 ==0) return false;
        return true;
    }
};