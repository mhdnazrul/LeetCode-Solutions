class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int ln = nums.size();
        for(int i = 0; i < ln; i++) {
            for(int j = i + 1; j < ln; j++) { 
                int sum = nums[i] + nums[j];
                if(sum == target){
                    return {i, j}; 
                }
            }
        }
        return {}; 
    }
};