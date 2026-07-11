class Solution {
public:
    static long long bin_refl(int x){
        long long ans=0;
        for(; x; x>>=1){
            ans+=(ans<<1LL)+(x&1);
        }
        return ans;
    }
    vector<int> sortByReflection(vector<int>& nums) {
        sort(nums.begin(), nums.end(), [&](int x, int y){
            return bin_refl(x)==bin_refl(y)?x<y:bin_refl(x)<bin_refl(y);
        });
        return nums;
    }
};