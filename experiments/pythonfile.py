from matplotlib.pyplot import imshow, draw, pause, show

import numpy as np # for linear algebra help
from math import inf, log2 # for math help :D
from random import randint, random # for random number generation
from skimage.metrics import structural_similarity, mean_squared_error # For similarity measurement
import cv2 # opencv2 for image management
from multiprocessing import Pool # To distribute processes
from pathlib import Path
from PIL import Image, ImageFilter # for initial image palette and bgcolor generation with help of colorthief
from colorthief import ColorThief # For grabbing color information from source image
import pickle # For saving checkpoints
import time

class NoAdjuster: # Default adjustment to image, does nothing.
    def adjust(self, originalImage):
        return originalImage

    def unadjust(self, originalImage):
        return originalImage

class DarkAdjuster: # An adjustment that improves sensitivity of algorithm to dark spots in image.
    def __init__(self):
        self.ADJUST_A = 17.1976
        self.ADJUST_B = 256
        self.ADJUST_C = 512
        self.ADJUST_D = -262.665
    

    def adjust(self, originalImage):
        # image is a numpy array
        adjustedImage = originalImage.copy()
        adjustedImage = adjustedImage + self.ADJUST_A
        adjustedImage = np.log(adjustedImage) / np.log(self.ADJUST_B)
        adjustedImage = adjustedImage * self.ADJUST_C
        adjustedImage = adjustedImage + self.ADJUST_D
        adjustedImage = np.rint(adjustedImage).astype(np.uint8)
        return adjustedImage


    def unadjust(self, adjustedImage):
        # image is a numpy array
        originalImage = adjustedImage.copy()
        originalImage = originalImage - self.ADJUST_D
        originalImage = originalImage / self.ADJUST_C
        originalImage = np.exp2(log2(self.ADJUST_B) * originalImage)
        originalImage = originalImage - self.ADJUST_A
        originalImage = np.rint(originalImage).astype(np.uint8)
        return originalImage



class SmoothPreprocessor: # A preprocessor that smooths the original image before processing.
    def preprocess(self, image):
        processedImage = image.filter(ImageFilter.SMOOTH_MORE)
        processedImage = processedImage.filter(ImageFilter.SMOOTH_MORE)
        processedImage = processedImage.filter(ImageFilter.SMOOTH_MORE)
        return processedImage

class NoPreprocessor: # A preprocessor that does nothing.
    def preprocess(self, image):
        return image


class MeanSquaredError: # A class that computes mean squared error
    def calculateError(self, image, source):
        return mean_squared_error(image, source)

class StructuralSimilarityError: # A class that computes structural similarity, as an error
    def calculateError(self, image, source):
        return -1 * structural_similarity(image, source, multichannel=True)



def changeColorFromRGBToBGR(color): # converts from RGB (colorthief colors) to BGR format (opencv2 colors)
    return (color[2], color[1], color[0])

def showImage(image, display=None, adjuster=NoAdjuster()): # Shows the image, this is placeholder for VSCode to Colab conversions (since cv2_imshow does not work outside of colab)
    restoredImage = adjuster.unadjust(image)
    restoredImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if display is None:
        display = imshow(restoredImage)
    else:
        display.set_data(restoredImage)

    draw()
    pause(0.01)
    return display

def addCircle(image, gene, palette): # Adds a circle based on gene information onto an image using opencv2 blending modes.
    overlay = image.copy()
    cv2.circle(
        overlay,
        center=gene.center,
        radius=gene.radius,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA # add antialiasing
    )
    cv2.addWeighted(overlay, gene.alpha, image, 1-gene.alpha, 0, image)

def getRescaleRatio(image, target): # Gets a rescale ratio based on an image and a target resolution
    # Target: 250x250
    width = image.width
    height = image.height

    if width <= target or height <= target:
        return 1

    ratio = target / min(width, height)
    return ratio

class ColorThiefFromImage(ColorThief): # Extend ColorThief to support providing images as-is instead of filenames
    def __init__(self, image):
        self.image = image

class Gene: # Defines a single gene, which describes how to draw a single circle.
    def __init__(self, maximumRadius, minimumRadius, height, width, numColors, radius=None, center=None, color=None, alpha=None): # Basic constructor.  Leave default parameters empty for randomization.
        self.maximumRadius = maximumRadius
        self.minimumRadius = minimumRadius
        self.height = height
        self.width = width
        self.numColors = numColors
        if radius is None:
            self.completelyRandomize() # Randomize values at initialization.
        else:
            self.radius = radius
            self.center = center
            self.color = color
            self.alpha = alpha
    
    def revert(self): # Reverts circle to previous properties (in case a mutation was unhelpful.)
        self.radius = self.history[0]
        self.center = self.history[1]
        self.color = self.history[2]
        self.alpha = self.history[3]
    
    def completelyRandomize(self): # Completely randomizes the values 
        self.randomizeRadius()
        self.randomizeCenter()
        self.randomizeColor()
        self.randomizeAlpha()

    def mutate(self, complete=False): # Mutates a circle randomly.  If complete is True, this will always perform a complete mutation.
        # backup
        self.history = [self.radius, self.center, self.color, self.alpha]

        # Chances of altering the radius or alpha
        radiusAlter = random() < 0.293
        alphaAlter = random() < 0.293

        # Whether an alteration still needs to be made
        noAlter = not (radiusAlter or alphaAlter)

        # Mutate.
        if radiusAlter:
            self.randomizeRadius()
        if alphaAlter:
            self.randomizeAlpha()
        if noAlter:
            self.completelyRandomize()
    
    def randomizeRadius(self): # randomizes radius
        self.radius = randint(self.minimumRadius, self.maximumRadius)
    
    def randomizeCenter(self): # randomizes center of circle
        self.center = (randint(0 - int(self.radius/5), self.width + int(self.radius/5)), randint(0 - int(self.radius/5), self.height + int(self.radius/5)))
    
    def randomizeColor(self): # randomizes color
        self.color = randint(0, self.numColors-2)
    
    def randomizeAlpha(self): # randomizes alpha
        self.alpha = random() * 0.45 + 0.05

    def getScaledVersion(self, ratio): # Creates a new gene that represents the circle scaled by some ratio.
        newRadius = int(self.radius / ratio)
        newCenter = (int(self.center[0] / ratio), int(self.center[1] / ratio))
        newHeight = int(self.height / ratio)
        newWidth = int(self.width / ratio)
        newMaxRadius = int(self.maximumRadius / ratio)
        newMinRadius = int(self.minimumRadius / ratio)
        return Gene(newMaxRadius, newMinRadius, newHeight, newWidth, self.numColors, newRadius, newCenter, self.color, self.alpha)

    def clone(self): # Creates a copy of itself.
        return Gene(self.maximumRadius, self.minimumRadius, self.height, self.width, self.numColors, self.radius, self.center, self.color, self.alpha)


class Genome: # Represents an entire image's circle sequence and properties.
    def __init__(self, sequence, ratio, height, width, backgroundColor, adjuster): # basic constructor
        self.sequence = sequence
        self.ratio = ratio
        self.height = height
        self.width = width
        self.backgroundColor = backgroundColor
        self.adjuster = adjuster
    
    def renderScaledImage(self): # render the image, scaled to its ratio.
        scaledHeight = int(self.height / self.ratio)
        scaledWidth = int(self.width / self.ratio)
        scaledSequence = self.scaleSequence()
        scaledImage = self.renderImage(scaledHeight, scaledWidth, scaledSequence)

        return scaledImage
    
    def scaleSequence(self): # scale each circle in the gene sequence by the ratio.
        return [gene.getScaledVersion(self.ratio) for gene in self.sequence]

    def renderRawImage(self): # render the image without scaling.
        return self.renderImage(self.height, self.width, self.sequence)
    
    def renderImage(self, height, width, sequence): # renders the image according to parameters.
        image = np.zeros((height, width, 3), np.uint8)
        image[:] = self.backgroundColor

        for gene in sequence:
            addCircle(image, gene, palette)
        return image
    
    def saveGenome(self, filename): # Saves the genome to a pickle file.
        with open(filename, 'wb') as genomeFile:
            pickle.dump(self, genomeFile)
    
    @staticmethod
    def loadGenome(filename): # Loads a genome from a pickle file.
        with open(filename, 'rb') as genomeFile:
            genome = pickle.load(genomeFile)
        return genome

def simpleMutation(image, baseImage, sequence, errorChecker, palette): # Computes the effects of a simple mutation.
    mutatedGene = sequence[0].clone()
    mutatedGene.mutate()
    newImage = image.copy()
    addCircle(newImage, mutatedGene, palette)
    error = errorChecker.calculateError(newImage, baseImage)
    return error, mutatedGene, newImage

def complexMutation(ancestorImage, baseImage, sequence, numCircles, errorChecker, palette): # computes the effects of a complex mutation.

    mutationIndex = randint(0, numCircles - 1)
    mutatedGene = sequence[mutationIndex].clone()
    mutatedGene.mutate()

    newImage = ancestorImage.copy()

    if random() > 0.5:
        for index, gene in enumerate(sequence):
            if index != mutationIndex:
                addCircle(newImage, gene, palette)
        addCircle(newImage, mutatedGene, palette)
        top = True

    else:
        for index, gene in enumerate(sequence):
            if index == mutationIndex:
                addCircle(newImage, mutatedGene, palette)
            else:
                addCircle(newImage, gene, palette)
        top = False
    
    error = errorChecker.calculateError(newImage, baseImage)
    return error, mutatedGene, newImage, mutationIndex, top

def getImagePath(name, directory):
    return str(Path(__file__).absolute().parent) + "\\" + directory + "\\" + name


if __name__ == '__main__':

    adjuster = NoAdjuster() # Default
    preprocessor = SmoothPreprocessor() # Default preprocessor: smooth
    errorChecker = MeanSquaredError() # Default error method: mean squared error

    # Trial filenames

    IMAGEDIRECTORY = "source-images"

    MONALISA = getImagePath("monalisa.jpg", IMAGEDIRECTORY)
    PEARLEARRING = getImagePath("pearlearring.jpg", IMAGEDIRECTORY)
    STARRYNIGHT = getImagePath("starrynight.png", IMAGEDIRECTORY)

    NUM_COLORS = 256 # Number of colors in color palette (this is approximate, colorthief is inconsistent)

    RESOLUTION = 250 # Default resolution for the algorithm.

    BASEIMAGE_FILENAME = STARRYNIGHT # Set this to filename of proper image


    baseImage = Image.open(BASEIMAGE_FILENAME) 

    processedImage = preprocessor.preprocess(baseImage)

    ratio = getRescaleRatio(processedImage, RESOLUTION)

    processedImage = processedImage.resize((int(processedImage.width * ratio), int(processedImage.height * ratio)), Image.LANCZOS)

    imageArray = np.asarray(processedImage)
    originalBaseImage = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR)

    imageArray = adjuster.adjust(imageArray)
    processedImage = Image.fromarray(imageArray)

    BGRbaseImage = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR) # This will be the image used for training the genome.

    imageArray = adjuster.unadjust(imageArray)
    restoredBaseImage = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR)

    # generate some colours out of smoothened image, and convert colours from RGB to BGR
    colorThief = ColorThiefFromImage(processedImage)
    backgroundColor = changeColorFromRGBToBGR(colorThief.get_color(quality=1)) # gets the background color
    palette = colorThief.get_palette(color_count=NUM_COLORS, quality=1) # gets the top colors used by the image.
    for index, color in enumerate(palette):
        palette[index] = changeColorFromRGBToBGR(color)

    display = showImage(BGRbaseImage) # Preview image

    # Set evolution constants

    NUM_GENERATIONS = 5000 # 4000 default. Number of generations to run.

    NUM_CIRCLES = 1000 # 1000 default. Number of circles to draw. 

    print("Shape of image: ")
    print(BGRbaseImage.shape)

    # Calculations for minimum and maximum radius to draw on images.
    MINIMUM_RADIUS = int(0.02 * min(BGRbaseImage.shape[:1]))
    MAXIMUM_RADIUS = int(0.08 * min(BGRbaseImage.shape[:1]))

    print("Minimum Circle Radius: ")
    print(MINIMUM_RADIUS)

    print("Maximum Circle Radius: ")
    print(MAXIMUM_RADIUS)

    # width and height variables for convenience.
    height = BGRbaseImage.shape[0]
    width = BGRbaseImage.shape[1]

    # Build a base image with a solid background color.
    ancestorImage = np.zeros((height, width, 3), np.uint8)
    ancestorImage[:] = backgroundColor

    showImage(ancestorImage, display=display) # Preview base image

    topScore = inf # original best score is infinite, so the first run will always overwrite it.
    topImage = None # the best image so far.

    cachedImage = None # Location to store a cached image for later use.
    recallFromCache = False # Whether to load an image from the cache or build it from scratch.


    start = time.time()


    sequence = [Gene(MAXIMUM_RADIUS, MINIMUM_RADIUS, height, width, NUM_COLORS) for _ in range(NUM_CIRCLES)] # Generate initial gene sequence.

    genome = Genome(sequence, ratio, height, width, backgroundColor, adjuster) # Build a genome



    EARLY_STOPPING_LIMIT = 25 # number of failed generations before an algorithm switches from simple to complex.
    generationsSinceLastChange = 0 # counter for above.

    totalGenerationChanges = 0 # number of total generation changes, used to determine how long an algorithm should stay complex.
    consecutiveExtremeMutations = 0 # counter for early stopping.
    EARLY_STOPPING_LIMIT_EXTREME_MUTATION = 1000 # limit on how many failed complex mutations can be run.
    extremeMutation = False # default value of whether to use extreme mutations.

    finalRun = False


    # Multiprocessing variables
    SIMPLE_POOL_SIZE = 32
    COMPLEX_POOL_SIZE = 4

    simplePool = Pool(SIMPLE_POOL_SIZE)
    complexPool = Pool(COMPLEX_POOL_SIZE)

    lastUpdate = -1

    generationIndex = 0
    offspring = 0 # Record number of generations.
    changes = 0 # Record number of total changes made. (some generations may have failed mutations that do not affect the sequence.)

    print("start")

    while changes < NUM_GENERATIONS:
        if extremeMutation:
            finalRun = False

            offspring += COMPLEX_POOL_SIZE

            results = complexPool.starmap(complexMutation, [(ancestorImage, BGRbaseImage, sequence, NUM_CIRCLES, errorChecker, palette) for _ in range(COMPLEX_POOL_SIZE)])
            scoreList = [results[index][0] for index in range(COMPLEX_POOL_SIZE)]
            bestIndex = scoreList.index(min(scoreList))
            score = results[bestIndex][0]
            mutatedGene = results[bestIndex][1]
            image = results[bestIndex][2]
            mutatedIndex = results[bestIndex][3]
            top = results[bestIndex][4]

            # If successful...
            if score < topScore:
                topScore = score
                topImage = image
                del sequence[mutatedIndex]
                if top:
                    sequence.append(mutatedGene)
                else:
                    sequence.insert(mutatedIndex, mutatedGene)
                changes += 1
                # Reset all values and go back to regular mutations.
                generationsSinceLastChange = 0
                consecutiveExtremeMutations += 1
                if (consecutiveExtremeMutations >= totalGenerationChanges ** 2):
                    recallFromCache = False
                    extremeMutation = False
            else:
                generationsSinceLastChange += 1
                # If we really can't get anywhere, then quit.
                if generationsSinceLastChange >= EARLY_STOPPING_LIMIT_EXTREME_MUTATION:
                    finalRun = True
                    generationsSinceLastChange = 0
                    recallFromCache = False
                    extremeMutation = False
                    print("early stop!")
                    break

        else:

            offspring += SIMPLE_POOL_SIZE

            # add the rest of the circles normally
            if recallFromCache:
                image = cachedImage.copy() # Take built image from 
            else:
                image = ancestorImage.copy()
                for index, gene in enumerate(sequence):
                    if index != 0:
                        addCircle(image, gene, palette)
                cachedImage = image.copy()
                recallFromCache = True

            results = simplePool.starmap(simpleMutation, [(image, BGRbaseImage, sequence, errorChecker, palette) for _ in range(SIMPLE_POOL_SIZE)])

            scoreList = [results[index][0] for index in range(SIMPLE_POOL_SIZE)]
            bestIndex = scoreList.index(min(scoreList))
            score = results[bestIndex][0]
            mutatedGene = results[bestIndex][1]
            image = results[bestIndex][2]



            # if it was beneficial...
            if score < topScore:
                topScore = score
                topImage = image

                del sequence[0]
                sequence.append(mutatedGene) # Place the gene on top of the sequence again.

                changes += 1 # record a change
                generationsSinceLastChange = 0
                recallFromCache = False # Build next image from scratch.
                finalRun = False
            else:
                generationsSinceLastChange += 1
                if generationsSinceLastChange >= EARLY_STOPPING_LIMIT:
                    totalGenerationChanges += 1
                    extremeMutation = True
                    generationsSinceLastChange = 0
                    consecutiveExtremeMutations = 0
                    if finalRun:
                        break

        generationIndex += 1
        
        # Periodic checks on progress, every 100 generations.
        if changes % 50 == 0 and lastUpdate != changes:
            lastUpdate = changes
            print(f"offspring: {offspring}")
            print(f"number of changes: {changes}")
            print(f"number of total generations: {generationIndex}")
            print(f"number of evolution switches: {totalGenerationChanges}")
            print(f"error: {topScore}")
            extreme = "extreme" if extremeMutation else "not extreme"
            print(f"Extreme?: {extreme}")
            showImage(topImage, display=display, adjuster=adjuster)

    
    end = time.time()

    print(f"Total time elapsed: {end - start}")


    showImage(topImage, display=display, adjuster=adjuster)

    showImage(genome.renderRawImage(), display=display, adjuster=genome.adjuster)

    image = genome.renderScaledImage()

    showImage(genome.renderScaledImage(), display=display, adjuster=genome.adjuster)

    cv2.imwrite(BASEIMAGE_FILENAME + "_result.png", image)

    genome.saveGenome(BASEIMAGE_FILENAME + "_genome.pkl")


    print("changes: ")
    print(changes)

    show()

