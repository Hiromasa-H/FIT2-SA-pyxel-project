from perlin_noise import PerlinNoise
import random

noise_index = 0
noise_resolution = 500

p_noise = PerlinNoise(octaves = 10, seed = random.randint(1,100))

while True:

  noise_index +=1
  if noise_index == noise_resolution:
    noise_index = 0

  noise = p_noise(noise_index/noise_resolution)


  print(round(noise*10))