class Solution {
public:
    long long rob(vector<int>& nums, vector<int>& colors) {
        int n = nums.size();
        
        long long notRobbed = 0;
        long long robbed = nums[0];
        
        for (int i = 1; i < n; i++) {
            long long nextNotRobbed = max(notRobbed, robbed);
            
            long long nextRobbed = notRobbed + nums[i];
            if (colors[i] != colors[i - 1]) {
                nextRobbed = max(nextRobbed, robbed + nums[i]);
            }
            
            notRobbed = nextNotRobbed;
            robbed = nextRobbed;
        }
        
        return max(notRobbed, robbed);
    }
};