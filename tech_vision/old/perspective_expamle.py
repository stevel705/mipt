
import numpy as np 
import cv2

def perspectiveTransform(perspectiveMatrix, sourcePoints):
    '''
    perspectiveMatrix as above
    sourcePoints has shape (n,2)
    '''
    # first we extend source points by a column of 1
    # augment has shape (n,1)
    augment = np.ones((sourcePoints.shape[0],1))
    # projective_corners is a 3xn matrix with last row all 1
    # note that we transpose the concatenation
    projective_corners = np.concatenate( (sourcePoints, augment), axis=1).T

    # projective_points has shape 3xn
    projective_points = perspectiveMatrix.dot(projective_corners)

    # obtain the target_points by dividing the projective_points 
    # by its last row (where it is non-zero)
    # target_points has shape (3,n).
    target_points = np.true_divide(projective_points, projective_points[-1])

    # print(projective_points)
    print(target_points)
    # so we want return points in row form
    return target_points[:2].T


if __name__=='__main__':
    # Create a transform to change table coordinates in inches to projector coordinates
    sourceCorners = np.array([[0.0, 0.0],[120.0,0.0],[120.0,63.0],[0.0,63.0]],dtype=np.float32)
    destinationCorners = np.array([[4095.0,0],[3071,4095],[1024,4095],[0,0]],dtype=np.float32)
    perspectiveMatrix = cv2.getPerspectiveTransform(sourceCorners, destinationCorners)

    # test points
    points = np.array([0,0,0,240,320,0,320,240], dtype=float)

    # perspectiveTransform by cv2
    cv_perspectivePoints = cv2.perspectiveTransform(points.reshape(-1,1,2), perspectiveMatrix)

    # our implementation of perspectiveTransform
    perspectivePoints = perspectiveTransform(perspectiveMatrix, points.reshape(-1, 2))
    print(perspectivePoints)
    # should yields something close to 0.0
    # print(cv_perspectivePoints.reshape(-1,2) - perspectivePoints)