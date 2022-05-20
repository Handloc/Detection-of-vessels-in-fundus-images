import math
from sklearn.metrics import confusion_matrix


def accuracy(perfect_img, image):
    image = image.reshape(-1)
    perfect_img = perfect_img.reshape(-1)
    cm = confusion_matrix(perfect_img, image)
    tp, fp, fn, tn = cm[0][0], cm[0][1], cm[1][0], cm[1][1]

    acc = (tp + tn) / (tp + tn + fp + fn)
    sens = tp / (tp + fn)
    spec = tn / (tn + fp)

    detected_true = 0
    detected_false = 0
    all_white = 0

    for i in range(len(image)):
        if perfect_img[i]:
            all_white += 1
            if image[i]:
                detected_true += 1
        else:
            if image[i]:
                detected_false += 1

    return f"TP: {tp}\tFP: {fp}\nFN: {fn}\tTN:{tn}\n\n" \
           f"Trafność: {acc}\nCzułość: {sens}\nSwoistość: {spec}\n\n" \
           f"Percentage true detected: {detected_true/all_white*100}\nPercentage false detected: " \
           f"{detected_false/(detected_true+detected_false)*100}\n" \
           f"Średnia arytmetyczna: {(tp / (tp + fn) + tn / (tn + fp)) / 2}\n" \
           f"Średnia geometryczna: {(math.sqrt(tp / (tp + fn)) * (tn / (tn + fp)))}"

