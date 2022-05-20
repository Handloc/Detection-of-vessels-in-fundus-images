from skimage import io
import wx
from accuracy import accuracy
from image_processing import image_processing
from classifier_learning import classifier_learning
from classifier_processing import classifier_processing


class GUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(GUI, self).__init__(*args, **kw)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.input_image_path = 0
        self.mask_path = 0
        self.perfect_image_path = 0

        self.image_mask_select = 0

        self.input_image_text = wx.StaticText(self.panel, label="Obraz wejściowy", style=wx.ALIGN_CENTER)
        self.perfect_image_text = wx.StaticText(self.panel, label="Obraz idealny", style=wx.ALIGN_CENTER)
        self.mask_text = wx.StaticText(self.panel, label="Obraz wyjściowy", style=wx.ALIGN_CENTER)

        self.left_margin = wx.StaticText(self.panel, label="")
        self.result_text = wx.StaticText(self.panel, label="")
        self.right_margin = wx.StaticText(self.panel, label="")

        image_processing_button = wx.Button(self.panel, wx.ID_ANY, "Technika przetwarzania obrazu", size=(200, 32))
        image_processing_button.Bind(wx.EVT_BUTTON, self.image_processing_button)

        classifier_learning_button = wx.Button(self.panel, wx.ID_ANY, "Uczenie klasyfikatora", size=(200, 32))
        classifier_learning_button.Bind(wx.EVT_BUTTON, self.button_classifier_learning)

        self.classifier_processing_button = wx.Button(self.panel, wx.ID_ANY, "Technika z użyciem klasyfikatora",
                                                      size=(200, 32))
        self.classifier_processing_button.Bind(wx.EVT_BUTTON, self.button_classifier_processing)
        self.classifier_processing_button.Disable()

        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        pathSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        variableSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowSizer = wx.BoxSizer(wx.VERTICAL)

        self.input_image = wx.Bitmap.FromRGBA(438, 292, alpha=255)
        self.mask = wx.Bitmap.FromRGBA(438, 292, alpha=255)
        self.perfect_image = wx.Bitmap.FromRGBA(438, 292, alpha=255)
        self.output = wx.Bitmap.FromRGBA(438, 292, alpha=255)

        self.inputImage = wx.StaticBitmap(self.panel, wx.ID_ANY, bitmap=self.input_image)
        self.idealImage = wx.StaticBitmap(self.panel, wx.ID_ANY, bitmap=self.perfect_image)
        self.outputImage = wx.StaticBitmap(self.panel, wx.ID_ANY, bitmap=self.output)
        self.inputImage.Bind(wx.EVT_LEFT_DOWN, self.image_mask_changer)

        headerSizer.Add(self.input_image_text, 1, wx.ALIGN_CENTER)
        headerSizer.Add(self.perfect_image_text, 1, wx.ALIGN_CENTER)
        headerSizer.Add(self.mask_text, 1, wx.ALIGN_CENTER)
        imageSizer.Add(self.inputImage, 1)
        imageSizer.Add(self.idealImage, 1)
        imageSizer.Add(self.outputImage, 1)

        buttonSizer.Add(image_processing_button, wx.SizerFlags().Border(wx.ALL, 5))
        buttonSizer.Add(classifier_learning_button, wx.SizerFlags().Border(wx.ALL, 5))
        buttonSizer.Add(self.classifier_processing_button, wx.SizerFlags().Border(wx.ALL, 5))

        variableSizer.Add(self.left_margin, 1, wx.ALIGN_CENTER)
        variableSizer.Add(self.result_text, 1, wx.ALIGN_CENTER)
        variableSizer.Add(self.right_margin, 1, wx.ALIGN_CENTER)

        windowSizer.Add(headerSizer, 0, wx.EXPAND | wx.ALL)
        windowSizer.Add(imageSizer, 1, wx.EXPAND | wx.ALL)
        windowSizer.Add(pathSizer, 0, wx.EXPAND | wx.ALL)
        windowSizer.Add(buttonSizer, 1, wx.ALIGN_CENTER)
        windowSizer.Add(variableSizer, 1, wx.EXPAND | wx.ALL)
        self.panel.SetSizer(windowSizer)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("")

    def makeMenuBar(self):
        fileMenu = wx.Menu()

        inputImageItem = fileMenu.Append(-1, "&Otwórz obraz wejściowy")
        maskImageItem = fileMenu.Append(-1, "Otwórz &maskę obrazu wejściowego")
        idealImageItem = fileMenu.Append(-1, "Otwórz &idealny obraz wynikowy")

        fileMenu.AppendSeparator()
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&Menu")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.open_input_image, inputImageItem)
        self.Bind(wx.EVT_MENU, self.open_mask, maskImageItem)
        self.Bind(wx.EVT_MENU, self.open_perfect_image, idealImageItem)

    def image_mask_changer(self, event):
        if self.image_mask_select == 0:
            self.inputImage.Bitmap = self.mask
            self.input_image_text.SetLabel("Maska obrazu wejściowego")
            self.image_mask_select = 1
        else:
            self.inputImage.Bitmap = self.input_image
            self.input_image_text.SetLabel("Obraz wejściowy")
            self.image_mask_select = 0
        self.panel.Layout()

    def image_processing_button(self, event):
        image_processing(self.input_image_path, self.mask_path)
        self.output = wx.Bitmap("output.png").ConvertToImage().Scale(438, 292, wx.IMAGE_QUALITY_HIGH)
        self.output = wx.Bitmap(self.output)
        self.perfect_image_text.SetLabel("Obraz idealny")
        self.mask_text.SetLabel("Obraz wyjściowy")
        self.idealImage.Bitmap = self.perfect_image
        self.outputImage.Bitmap = self.output
        perfect_image = io.imread(self.perfect_image_path, as_gray=True)
        output_image = io.imread("output.png", as_gray=True)
        dat = accuracy(perfect_image, output_image)
        self.result_text.SetLabel(dat)
        self.panel.Layout()

    def button_classifier_learning(self, event):
        classifier_learning()
        self.classifier_processing_button.Enable()

    def button_classifier_processing(self, event):
        classifier_processing(self.input_image_path, self.mask_path)
        self.output = wx.Bitmap("output.png").ConvertToImage().Scale(438, 292, wx.IMAGE_QUALITY_HIGH)
        self.perfect_image_text.SetLabel("Obraz idealny")
        self.mask_text.SetLabel("Obraz wyjściowy")
        self.idealImage.Bitmap = self.perfect_image
        self.output = wx.Bitmap(self.output)
        self.outputImage.Bitmap = self.output
        perfect_image = io.imread(self.perfect_image_path, as_gray=True)
        output_image = io.imread("output.png", as_gray=True)
        dat = accuracy(perfect_image, output_image)
        self.result_text.SetLabel(dat)
        self.panel.Layout()

    def file_dialog(self):
        with wx.FileDialog(self, "Wybierz obraz",
                           wildcard="Obrazy (*.png;*.bmp;*.gif;*.jpg;*.jpeg;*.tiff;*.tif)|"
                                    "*.png;*.bmp;*.gif;*.jpg;*.jpeg;*.tiff;*.tif",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return 0
            return fileDialog.GetPath()

    def open_input_image(self, event):
        self.input_image_path = self.file_dialog()
        if self.input_image_path != 0:
            self.input_image = wx.Bitmap(self.input_image_path).ConvertToImage().Scale(438, 292, wx.IMAGE_QUALITY_HIGH)
            self.input_image = wx.Bitmap(self.input_image)
            self.inputImage.Bitmap = self.input_image
            self.input_image_text.SetLabel("Obraz wejściowy")
            self.image_mask_select = 0
            self.panel.Layout()

    def open_mask(self, event):
        self.mask_path = self.file_dialog()
        if self.mask_path != 0:
            self.mask = wx.Bitmap(self.mask_path).ConvertToImage().Scale(438, 292, wx.IMAGE_QUALITY_HIGH)
            self.mask = wx.Bitmap(self.mask)
            self.inputImage.Bitmap = self.mask
            self.input_image_text.SetLabel("Maska obrazu wejściowego")
            self.image_mask_select = 1
            self.panel.Layout()

    def open_perfect_image(self, event):
        self.perfect_image_path = self.file_dialog()
        if self.perfect_image_path != 0:
            self.perfect_image = wx.Bitmap(self.perfect_image_path).ConvertToImage().Scale(438, 292,
                                                                                           wx.IMAGE_QUALITY_HIGH)
            self.perfect_image = wx.Bitmap(self.perfect_image)
            self.perfect_image_text.SetLabel("Obraz idealny")
            self.mask_text.SetLabel("Obraz wyjściowy")
            self.outputImage.Bitmap = self.output
            self.idealImage.Bitmap = self.perfect_image
            self.panel.Layout()
