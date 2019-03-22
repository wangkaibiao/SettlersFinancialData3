webcam 的数据 训练神经网络模型来预测
作者：黑胡桃实验室 / 公众号：blackwalnutlabs 发布时间：2019-02-08

作者：TensorFlow.js 团队
在 TensorFlow.js 的核心概念 中，我们学会了使用 Tensor（张量）和 Ops（操作）去执行基本的线性代数运算。
在 图像训练：用卷积神经网络识别手写数字 中，我们学会了如何构建一个卷积图像分类器去识别 MNIST 数据集中的手写数字图片。
在 导入 Keras 模型教程 中，我们学会了如何将预训练好的 Keras 模型移植到浏览器中使用。
在本教程中，我们将使用迁移学习来玩 Pacman。从 webcam 读取数据（姿势、对象、面部表情等），然后将这些姿势数据进行预测后归类到“向上”、“向下”、“向左”、“向右”，完成用户定义的 class（类别）。
1关于这个游戏
这个游戏分三个步骤：
1. 数据采集
玩家通过 webcam 上传“上、下、左、右”四个 class（类别）的图片数据。
2.训练
用输入的图片训练一个神经网络模型来预测。
3.预测/玩游戏
从 webcam 接收数据，用我们刚刚训练好的模型预测这些数据属于“上、下、左、右”中的哪个 class（类别），然后将预测结果传递给 Pacman 游戏。
2关于模型
为了在合理的时间内从 webcam 中分类不同的图像 class（类别），我们将重新训练或微调一个预训练的 MobileNet 模型，并且使用内部激活层的输出（MobileNet 模型内部的输出层）作为我们新模型的输入。
所以，我们实际上有两个模型：
第一个模型是预训练好的 MobileNet 模型被截断后输出一个内部激活层，我们将这个模型称为“被截断的 MobileNet 模型”，我们没有对这个模型进行训练。
第二个模型是将被截断的 MobileNet 模型的内部激活层的输出作为输入，然后预测“上、下、左、右”这四个 class（类别）中每一个的概率。我们对这个模型在浏览器中进行了训练。
通过使用被截断的 MobileNet 模型的内部激活层，我们可以使用已经训练好的 MobileNet 模型的 feature（特征），并通过相对较少时间的重训练来预测 1000 个 class（类别）的图片。
3关于教程
在本地运行这个项目，您需要安装以下依赖:
Node.js V8.9 或更高版本
Yarn 或者 NPM CLI
以下安装命令使用了 Yarn，当然如果您熟悉 NPM CLI 或更喜欢使用它，仍然可以使用 NPM CLI。
您可以通过克隆这个 repository 并构建 demo 来运行示例代码：
git clone https://github.com/tensorflow/tfjs-examples
cd tfjs-examples/webcam-transfer-learning
yarn
yarn watch
上述命令中的“tfjs-examples/webcam-transfer-learning”这个案例目录是各自独立不相干的，您可以复制这些案例来开始自己的项目。
注意：这种方法与 Teachable Machine 采用的方法不同。 Teachable Machine 使用 K-最近邻算法（KNN）对预训练的 SqueezeNet 模型得到的预测结果进行分类，而这种方法用从 MobileNet 模型的内部激活层的输出截取数据，然后传递给第二个神经网络进行训练。KNN 图像分类器在较少量的数据下工作得更好，但传递数据的神经网络有更好的泛化能力。让我们试一试两个 Demo，并探索两种不同方法构建的 webcam 预测有什么不同！
4数据
在开始训练我们的模型之前，我们需要一个方法从 webcam 取回 Tensor。
我们在 webcam.js 提供了一个叫 Webcam 的类别，它从 <video> 标签中读取图像作为 TensorFlow.js 的 Tensor。
让我们来看看 Webcam 中的 capture 方法。
capture() {
return tf.tidy(() => {
const webcamImage = tf.fromPixels(this.webcamElement);
const croppedImage = this.cropImage(webcamImage);
const batchedImage = croppedImage.expandDims(0);
return batchedImage.toFloat().div(oneTwentySeven).sub(one);
});
}
让我们逐行解析代码：
const webcamImage = tf.fromPixels(this.webcamElement);
这行代码从 webcam 的<video> 标签逐帧读取图像，并且返回 shape 为 [height, width, 3] 的 Tensor。其中 3 表示图像的 RGB 三个通道。
关于支持输入的 HTML 元素的类型，请参阅 tf.fromPixels 的文档。
const croppedImage = this.cropImage(webcamImage);
由于将 webcam 元素设置成正方形，webcam 返回的原始宽高比为矩形（浏览器会在矩形图像填充白色区域以使其成为正方形）。
MobileNet 模型的输入图像需要是正方形的。这行代码的意思是从 webcam 元素中抠取出一个大小为 [224, 224] 的正方形中心块。请注意， Webcam 中有很多代码可以增加视频元素的大小，因此我们可以裁剪一个正方形 [224, 224]，而不会被填充白色。
const batchedImage = croppedImage.expandDims(0);
expandDims这个方法可以创建一个新的大小为 1 的外部维度。在这种情况下，我们从 webcam 读取的图像的 shape 为 [224, 224, 3]。调用 exexpandDims(0) 将此张量（Tensor）的 shape 重新整理为 [1, 224, 224, 3]，它代表一个 batch（批次）的单图像。MobileNet 适合批量输入。
batchedImage.toFloat().div(tf.scalar(127)).sub(tf.scalar(1));
在这一行代码中，我们将图像数据转换为浮点，并作标准化处理，使数值大小保持在 -1 和 1 之间（这就是模型的训练方式）。默认情况下图像中的值介于 0 到 255 之间，因此为了在 -1 和 1 之间进行归一化，我们除以 127 并减去 1。
return tf.tidy(() => {
...
});
通过调用 tf.tidy() 告诉 TensorFlow.js 销毁我们在 capture() 中分配给中间 Tensor 的内存。有关内存管理和 tf.tidy() 的更多信息，请参阅 核心概念教程。
5加载 MobileNet 模型
在建立模型之前，我们需要将预先训练的 MobileNet 加载到网页中。从这个模型中，我们将从 MobileNet 内部激活层的输出构建一个新模型。
下面是实现的代码：
async function loadMobilenet() {
const mobilenet = await tf.loadModel('https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.25_224/model.json');
// 返回一个输出的内部激活层的模型。
const layer = mobilenet.getLayer('conv_pw_13_relu');
return tf.model({inputs: mobilenet.inputs, outputs: layer.output});
});
通过调用 getLayer('conv_pw_13_relu') 方法，我们将进入预训练的 MobileNet 模型的内部层并构建一个新模型。这个新模型的输入和 MobileNet 相同，但输出层是 MobileNet 的中间层 ，被称为 conv_pw_13_relu。
注意：我们是根据经验选择了这一层——它适用于我们的任务。一般而言，面向预训练模型的末尾层将在传递学习任务中表现更好，因为它包含输入的更高级的 semantic feature（语义特征）。您可以尝试选择另一个层，看看它如何影响模型质量！并且可以使用 model.layers 打印模型的图层。
注意：关于如何将 Keras 模型移植到 TensorFlow.js 的详细信息，请查看导入Keras模型教程。
6阶段 1: 收集数据
游戏的第一阶段是数据收集。用户将从 webcam 保存图像数据并与“上、下、左、右”四个 class（类别）中的每一个相关联。
当我们从 webcam 收集图像数据时，我们将立即把图像数据传入截断的 MobileNet 模型，并保存激活 tensor（张量）。我们不需要保存从 webcam 捕获的原始图像，因为我们模型的训练只需要这些激活数据作为输入。之后，当我们用 webcam 进行预测来实际玩游戏时，我们将首先给截断的 MobileNet 模型提供图像数据，然后把截断的 Mobilenet 模型的输出提供给我们的第二个模型。
我们提供了一个 ControllerDataset类，它可以保存这些激活数据，以便在训练阶段使用它们。 ControllerDataset有一个方法 addExample，将通过我们截断的 MobileNet 中激活的 Tensor和相对应 label（标签）作为 number（数字）来调用。
当新的 example（样本） 被添加，我们将保留两个表示整个数据集 xs 和 ys 的 Tensor（张量）用于模型训练的输入。
xs 表示采集的数据经过截断的 MobileNet 后输出的激活； ys 采用 “one hot” representation（用以表示非常长的向量）表示所有数据的对应标签。当我们训练模型时，我们通过 xs 和 ys 来提供给整个数据集。
让我们来看代码实现：
addExample(example, label) {
const y = tf.tidy(() => tf.oneHot(tf.tensor1d([label]), this.numClasses));
if (this.xs == null) {
this.xs = tf.keep(example);
this.ys = tf.keep(y);
} else {
const oldX = this.xs;
this.xs = tf.keep(oldX.concat(example, 0));
const oldY = this.ys;
this.ys = tf.keep(oldY.concat(y, 0));
oldX.dispose();
oldY.dispose();
y.dispose();
}
}
让我们来拆解分析这个方法。
const y = tf.tidy(() => tf.oneHot(tf.tensor1d([label]), this.numClasses));
该行用于把对应标签的整数转换为该标签的 One-Hot representation。
例如，如果 label = 1 对应于“left” class（类别），则 One-Hot representation 是 [0, 1, 0, 0]。我们做了这个转换用来代表概率分布，所以我们 100% 认为是 class 1（类别 1），向左。
if (this.xs == null) {
this.xs = tf.keep(example);
this.ys = tf.keep(y);
}
当我们添加第一个 example（样本） 到数据集时，就只保留给定的值。
我们对输入的 Tensor 调用 tf.keep()，这样它们就不会被任何可能包裹着 addExample 的 tf.tidy() 处理。
} else {
const oldX = this.xs;
this.xs = tf.keep(oldX.concat(example, 0));
const oldY = this.ys;
this.ys = tf.keep(oldY.concat(y, 0));
oldX.dispose();
oldY.dispose();
y.dispose();
}
当我们已经在数据集中增加了一个 example（样本），我们将会把 axis 参数设置为 0 并通过调用 concat 方法把这个新 example（样本） 连接到现有 example（样本） 中。不断将输入激活层加到 xs 中，同时将标签加到 ys 中，然后用 dispose() 方法处理之前所有的 xs 和 ys 值。
例如，如果我们的第一个标签（1）看起来像：
[[0, 1, 0, 0]]
然后我们对参数 label = 2 第二次调用 addExample 方法时， ys 将会变换为：
[[0, 1, 0, 0],
[0, 0, 1, 0]]
xs 将具有相似的 shape 但会有更高的维度，因为我们使用的是三通道激活层（这使得 xs 为四维的数据，其中最外层维度是收集的示例数）。
现在，我们回到定义核心逻辑的 index.js，在那里我们定义了以下内容：
ui.setExampleHandler(label => {
tf.tidy(() => {
const img = webcam.capture();
controllerDataset.addExample(mobilenet.predict(img), label);
// ...
});
});
在这个代码块中，我们注册了一个 UI 处理程序，当我们点击了任意一个“向上”、“向下”、“向左”、“向右”按钮，就会调用这段程序进行处理。其中“向上”、“向下”、“向左”、“向右”的标签（label）分别对应 class（类别）0、1、2、3。
在这个处理程序中，我们从 webcam 捕获一帧图像，并传递给 MobileNet 模型，从模型的内部激活层截取结果，然后将它保存在 ControllerDataset对象中。
7阶段 2: 训练模型
一旦从 webcam 中收集完四个 class（类别）数据的所有 example（样本） ，我们就可以训练我们的模型了！
首先，让我们建立模型架构。我们将创建一个拥有 2 层 Dense Layer（全连接层）的模型，第一个 dense layer（全连接层）后有 relu激活函数。
model = tf.sequential({
layers: [
// Flattens 是一个展平层，将输入的向量展平后使我们能在 dense layer（全连接层）中接收使用
// 从技术上来讲 Flattens 仅仅改变 Shape，没有训练参数
tf.layers.flatten({
inputShape: [7, 7, 256]
}),
tf.layers.dense({
units: ui.getDenseUnits(),
activation: 'relu',
kernelInitializer: 'varianceScaling',
useBias: true
}),
// 最后一层的神经数应该对应到我们想要预测的 class（类别）数
tf.layers.dense({
units: NUM_CLASSES,
kernelInitializer: 'varianceScaling',
useBias: false,
activation: 'softmax'
})
]
});
您会注意到模型的第一层实际上是一个 flatten（展平层）。我们需要将输入展平为向量，以便我们可以在 dense layer（全连接层）中使用。flatten（展平层）的 inputShape参数对应于我们被截断的 MobileNet 模型中的激活层输出的 shape。
我们要添加的下一层是一个 dense layer（全连接层）。我们将使用用户在页面中上传的图片，对其进行初始化，使用 relu 激活函数，使用 varianceScaling内核初始化，并且添加 bias（偏差）。
接着我们要添加的最后一层是另一个 dense layer（全连接层）。我们将使用与我们想要预测的 class（类别）数相对应的单位数来初始化它。然后使用 softmax作为激活函数，这意味着我们将最后一层的输出解释为可能的 class（类别）的概率分布。
关于层构造函数参数的详细信息可以查看 API 参考文档或图像训练：用卷积神经网络识别手写数字。
const optimizer = tf.train.adam(ui.getLearningRate());
model.compile({
optimizer: optimizer,
loss: 'categoricalCrossentropy'
});
这是我们准备进行训练的地方，构建优化器，定义损失函数以及编译模型。
这段代码中，我们使用了 Adam优化器，它可以很好地完成这项任务。 损失函数 categoricalCrossentropy 将计算 4 个 class（类别）预测的概率分布与真实标签（即 One-Hot encoding label）之间的误差。
const batchSize =
Math.floor(controllerDataset.xs.shape[0] * ui.getBatchSizeFraction());
由于我们的数据集是动态的（根据用户上传的图像确定训练的数据集大小），所以需要相应地调整 batch size（批次大小）。用户可能不会收集数千个 example（样本），因此 batch size（批次大小）可能不会太大。
现在，让我们来训练这个模型吧！
model.fit(controllerDataset.xs, controllerDataset.ys, {
batchSize,
epochs: ui.getEpochs(),
callbacks: {
onBatchEnd: async (batch, logs) => {
// 记录每一个 batch 中训练数据集的 cost（成本，即损失）。
ui.trainStatus('Cost: ' + logs.loss.toFixed(5));
await tf.nextFrame();
}
}
});
model.fit 函数可以将整个数据集作为 xs 和 ys，我们可以集中控制数据的传递。
我们在 UI 中设置了 epochs，允许用户定义训练模型的时间。我们还注册了一个 onBatchEnd回调函数，该函数在 fit内部循环训练时，每当一个 batch（批次）完成训练后调用。这个函数允许我们在模型训练时向用户显示中间 cost（成本，即损失）值。我们使用 await tf.nextFrame() 等待下一个画面允许 UI 在训练期间依旧能够更新。
有关此损失函数的更多详细信息，请参阅图像训练：用卷积神经网络识别手写数字。
8阶段3: 开始 Pacman
当我们的模型训练完成，并且我们的 cost（成本，即损失）值已经下降，我们就可以通过 webcam 进行预测！
下面是预测的循环：
while (isPredicting) {
const predictedClass = tf.tidy(() => {
const img = webcam.capture();
const activation = mobilenet.predict(img);
const predictions = model.predict(activation);
return predictions.as1D().argMax();
});
const classId = (await predictedClass.data())[0];
predictedClass.dispose();
ui.predictClass(classId);
await tf.nextFrame();
}
让我们逐行分析这些代码：
const img = webcam.capture();
正如我们之前所见，这段代码会从 webcam 捕获一帧图像作为一个 Tensor。
const activation = mobilenet.predict(img);
现在，把那一帧图像传入被截断的 MobileNet 模型，得到 MobileNet 模型的内部激活层。
const predictions = model.predict(activation);
在这行代码中，我们使用上一行代码中获取得到的 MobileNet 模型的内部激活层来预测。这将回输出 4 个 class（类别）的概率分布（这 4 个中的每一个预测向量代表该 class 的概率）。
predictions.as1D().argMax();
最后调用 argMax 函数后 flatten（展平）输出，这个过程将返回概率最高的Index，每一个Index对应一个预测的 class（类别）。
const classId = (await predictedClass.data())[0];
predictedClass.dispose();
ui.predictClass(classId);
现在我们有一个带有预测结果的 Tensor，我们需要在页面中显示它的内容！（注意我们需要在获取其值后手动处理 Tensor，因为我们无法在包含 tf.tidy() 的语句中进行异步操作）。
9尾声
现在！您已经学会了如何在浏览器中训练神经网络并对用户定义的 class（类别）进行预测，并且图像永远不会离开浏览器！
如果您 fork 了这个 demo 来进行修改，那么您可能需要更改模型参数才能兼容您的代码。
�7�2----------------------------------
本文是黑胡桃实验室与 Googler、GDE 协作翻译的 TensorFlow.js 中文尝鲜版，英文版首发于 https://js.tensorflow.org/

探索AI
触摸科技
黑胡桃实验室
杭州·赛银国际广场4幢1楼