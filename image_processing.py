from skimage import io, filters, morphology, measure, img_as_ubyte


def image_processing(input_path, mask_path):
    image = io.imread(input_path)
    mask = io.imread(mask_path, as_gray=True)
    image = image[:, :, 1]
    mask_2 = image < 135
    mask = mask * mask_2
    image = filters.gaussian(image, sigma=4.5)
    image = filters.frangi(image, sigmas=0.5)
    image = morphology.dilation(image)
    image = morphology.dilation(image)
    image = image > 0.00000000001
    image = morphology.erosion(image)
    image = morphology.erosion(image)
    image = morphology.dilation(image)
    image = morphology.dilation(image)
    image = filters.gaussian(image, sigma=3.5)
    image = image > 0.55
    image = image * mask
    image = morphology.remove_small_objects(measure.label(image.copy()), min_size=50000, connectivity=50000) > 0
    image = img_as_ubyte(image)
