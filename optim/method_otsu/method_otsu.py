# Для сравнения можно воспользоваться функцией cv2.threshold с параметром cv2.THRESH_OTSU
# 
import sys, os.path, cv2, numpy as np
import pylab as plt
import time

def otsu(img: np.ndarray) -> np.ndarray:
    threshold = -1
    var_max = -1
    sum = 0
    sumB = 0
    q1 = 0 
    q2 = 0

    max_intensity = 255
    N = img.shape[0] * img.shape[1]
    
    output_image = img.copy()
    
    hist = [0] * (max_intensity + 1)

    width = range(img.shape[0])
    height = range(img.shape[1])
    max_intensity_list = range(max_intensity + 1)
    
    # compute the image histogram
    for i in width:
        for j in height:
            value = img[i,j]
            hist[value] += 1
    
    # auxiliary value for computing m2
    for i in max_intensity_list:
        sum += i * hist[i]

    for t in max_intensity_list:
        # update qi(t)
        q1 += hist[t] 
        if q1 == 0:
            continue

        q2 = N - q1
        if q2 == 0:
            continue
        
        # update mi(t)
        sumB += t * hist[t] 
        m1 = sumB / q1
        m2 = (sum - sumB) / q2

        # update the between-class variance
        sigm2 = q1 * q2 * ((m1 - m2) * (m1 - m2))

        # update the threshold
        if sigm2 > var_max:
            threshold = t
            var_max = sigm2
    
    # find the max value index 
    # maxValue = 0
    # maxValueIndex = 0
    # for i in range(max_intensity + 1):
    #     if hist[i] > maxValue:
    #         maxValue = hist[i]
    #         maxValueIndex = i     

    # build the segmented image
    for i in width:
        for j in height:
            if img[i,j] > threshold:
                output_image[i, j] = 255
            else:
                output_image[i, j] = 0

    # plt.plot(hist)                                      
    # # plt.axvline(x=maxValueIndex, color='red', label='otsu') 
    # plt.legend(loc='upper right')                           
    # plt.title("histgram of brightness")                     
    # plt.xlabel("brightness")                                
    # plt.ylabel("frequency")                                 
    # plt.xlim([0, 256])                                      
    # plt.show()

    return output_image


def main():
    assert len(sys.argv) == 3
    src_path, dst_path = sys.argv[1], sys.argv[2]

    assert os.path.exists(src_path)
    img = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
    assert img is not None
    # start_time = time.time()
    result = otsu(img)
    # print("--- %s seconds ---" % (time.time() - start_time))
    cv2.imwrite(dst_path, result)


if __name__ == '__main__':
    main()
