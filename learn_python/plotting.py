# Plotting practise
import matplotlib.pyplot as plt

# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()

x_data = [1, 2, 3, 4]
y_data = [8, 4, 13, 28]
plt.figure(figsize=(9, 3))  # set the entire figure (including axes etc) to fit witin 9x3 inches
plt.plot(x_data, y_data, 'g.')  # draw green dots
plt.ylabel('1 to 4')
plt.xlabel('9 to six')
plt.axis([0, 10, 4, 30]) # increase the min, max values that the axis goes up to for xmin, xmax and ymin, yMax
plt.show()

# lets make a figure composed to two subplots
plt.figure(figsize=(4, 4))  # moderately sized drawing area
plt.subplot(2, 1, 1)  # new graph in the figure at row=2, col=1, index=1
plt.title('Awesome Graph1')
plt.ylabel('y')
plt.xlabel('x')
plt.plot([1, 2, 3], [4, 5, 6], 'r+')
plt.subplot(2, 1, 2)  # new graph in the figure at row=2, col=1, index=2
plt.title('Awesome Graph Dos')
plt.ylabel('y for subplot 2')
plt.xlabel('x label for subplot2')
plt.text(100, 50, 'one hunnid') # x=100, y=50
plt.plot([1, 100, 200], [100, 50, 1])
plt.show()

plt.close('all')