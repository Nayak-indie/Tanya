! Tanya - Numerical Computing Module (Fortran)
! High-performance statistical computations

module tanya_math
    implicit none
    
    ! Parameters
    integer, parameter :: dp = selected_real_kind(15, 307)
    
contains

    ! Calculate mean of array
    function calc_mean(arr) result(mean)
        real(dp), intent(in) :: arr(:)
        real(dp) :: mean
        mean = sum(arr) / size(arr)
    end function calc_mean

    ! Calculate standard deviation
    function calc_std(arr) result(std)
        real(dp), intent(in) :: arr(:)
        real(dp) :: std, mean, variance
        mean = calc_mean(arr)
        variance = sum((arr - mean)**2) / size(arr)
        std = sqrt(variance)
    end function calc_std

    ! Calculate TF-IDF score
    function tf_idf(tf, df, N) result(score)
        real(dp), intent(in) :: tf, df
        integer, intent(in) :: N
        real(dp) :: idf, score
        idf = log(real(N, dp) / (df + 1.0_dp))
        score = tf * idf
    end function tf_idf

    ! Simple linear regression
    subroutine linear_regression(x, y, n, slope, intercept, r_squared)
        real(dp), intent(in) :: x(:), y(:)
        integer, intent(in) :: n
        real(dp), intent(out) :: slope, intercept, r_squared
        real(dp) :: sum_x, sum_y, sum_xy, sum_x2, sum_y2
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x * y)
        sum_x2 = sum(x * x)
        sum_y2 = sum(y * y)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        ! R-squared calculation
        r_squared = ((n * sum_xy - sum_x * sum_y)**2) / &
                    ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    end subroutine linear_regression

    ! Keyword frequency analysis
    subroutine keyword_frequency(text, keywords, counts)
        character(len=*), intent(in) :: text
        character(len=*), intent(in) :: keywords(:)
        integer, intent(out) :: counts(size(keywords))
        integer :: i
        
        counts = 0
        do i = 1, size(keywords)
            counts(i) = index(lower_case(text), lower_case(keywords(i)))
            if (counts(i) > 0) counts(i) = 1
        end do
    end subroutine keyword_frequency

    function lower_case(str) result(lc)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: lc
        integer :: i, diff
        diff = iachar('a') - iachar('A')
        lc = str
        do i = 1, len(str)
            if (lc(i:i) >= 'A' .and. lc(i:i) <= 'Z') then
                lc(i:i) = char(iachar(lc(i:i)) + diff)
            end if
        end do
    end function lower_case

end module tanya_math

program main
    use tanya_math
    implicit none
    
    ! Example: keyword trend analysis
    real(dp) :: dates(10), frequencies(10)
    real(dp) :: slope, intercept, r_squared
    integer :: counts(3)
    character(len=100) :: sample_text
    character(len=20), dimension(3) :: keywords = ["AI      ", "news    ", "update  "]
    
    ! Sample data
    dates = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    frequencies = [10.0, 15.0, 14.0, 18.0, 25.0, 23.0, 30.0, 28.0, 35.0, 40.0]
    
    print *, "Tanya Fortran Computing Module"
    print *, "==============================="
    
    ! Linear regression for trend
    call linear_regression(dates, frequencies, 10, slope, intercept, r_squared)
    print *, "Trend: slope =", slope, ", intercept =", intercept
    print *, "R-squared =", r_squared
    
    ! Keyword frequency
    sample_text = "AI is great. News about AI is breaking. Update on AI available."
    call keyword_frequency(sample_text, keywords, counts)
    print *, "Keyword counts:", counts
    
    print *, "Mean frequency:", calc_mean(frequencies)
    print *, "Std deviation:", calc_std(frequencies)

end program main
