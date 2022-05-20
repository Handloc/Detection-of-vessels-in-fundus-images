from skimage import io
import numpy as np

from scipy.stats import moment

globalModel = 0


def classifier_processing(input_path, mask_path):
    mask_to_test = io.imread(mask_path, as_gray=True)
    image_to_test = io.imread(input_path)

    image_to_test = image_to_test[:, :, 1]
    h, w = image_to_test.shape[0], image_to_test.shape[1]

    PATCH_SIZE = 5
    HALF_PATCH_SIZE = 2
    TEST_OFFSET = 1
    outputArray = np.zeros((h, w), dtype=np.uint8)

    for row in range(0, h - PATCH_SIZE, TEST_OFFSET):

        test_list = []

        for col in range(0, w - PATCH_SIZE, TEST_OFFSET):
            patch = image_to_test[row:(row + PATCH_SIZE), col:(col + PATCH_SIZE)]
            m = moment(patch, [2, 3], axis=None)
            test_list.append([np.mean(patch), m[0], m[1]])
        y_pred = globalModel.predict(np.array(test_list))

        for p, i in enumerate(range(0, w - PATCH_SIZE, TEST_OFFSET)):
            if mask_to_test[row, i] == 0:
                continue
            outputArray[row + HALF_PATCH_SIZE, i + HALF_PATCH_SIZE] = round(255 * y_pred[p])

    io.imshow(outputArray)
