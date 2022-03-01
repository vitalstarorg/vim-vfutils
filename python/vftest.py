#print("Hello from Python source code!")
import unittest
import sys
import urllib, urllib.request
import json
from leadercmd import *

class Sample:
  def _get(url):
      return urllib.request.urlopen(url, None, 5).read().strip().decode()
  
  def _get_country():
      try:
          ip = Sample._get('http://ipinfo.io/ip')
          json_location_data = Sample._get('http://api.ip2country.info/ip?%s' % ip)
          location_data = json.loads(json_location_data)
          return location_data['countryName']
      except Exception as e:
          print('Error in sample plugin (%s)' % e.msg)
  
  def print_country():
      print('You seem to be in %s' % Sample._get_country())
  
  def insert_country():
      import vim
      row, col = vim.current.window.cursor
      current_line = vim.current.buffer[row-1]
      new_line = current_line[:col] + Sample._get_country() + current_line[col:]
      vim.current.buffer[row-1] = new_line


def run_unittest():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVimPlugin))
  suite.addTest(unittest.makeSuite(TestLeaderCmd))
  runner = unittest.TextTestRunner()
  runner.run(suite)


class TestVimPlugin(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()

