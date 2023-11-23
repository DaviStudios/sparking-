class Interpreter:
  def __init__(self):
      self.variables = {}

  def execute_line(self, line):
      if "prom" in line:
          self.handle_variable_declaration(line)
      elif "print" in line:
          self.handle_print_statement(line)
      elif "if" in line:
          self.handle_if_statement(line)

  def handle_variable_declaration(self, line):
      parts = line.split(" ")
      var_name = parts[1]
      var_value_str = ' '.join(parts[3:])
      if var_value_str.isdigit() or self.is_float(var_value_str):
          self.variables[var_name] = float(var_value_str)

  def is_float(self, s):
      try:
          float(s)
          return True
      except ValueError:
          return False

  def handle_print_statement(self, line):
      parts = line.split("print ")
      to_print = parts[1].strip()
      if '+' in to_print or '-' in to_print or '*' in to_print or '/' in to_print:
          result = self.evaluate_expression(to_print)
          if result is not None:
              print(result)
      elif to_print[0] == '"' and to_print[-1] == '"':
          print(to_print[1:-1])
      elif to_print in self.variables:
          print(int(self.variables[to_print]))

  def evaluate_expression(self, expression):
      elements = expression.split()
      operand_stack = []
      operator_stack = []
      for elem in elements:
          if elem in self.variables:
              operand_stack.append(self.variables[elem])
          elif elem.isdigit() or (elem[0]=='-' and elem[1:].isdigit()):
              operand_stack.append(int(elem))
          elif elem in ['+', '-', '*', '/']:
              while (len(operator_stack) > 0 and self.precedence(operator_stack[-1]) >= self.precedence(elem)):
                  op = operator_stack.pop()
                  num2 = operand_stack.pop()
                  num1 = operand_stack.pop()
                  if op == '+':
                      operand_stack.append(num1 + num2)
                  elif op == '-':
                      operand_stack.append(num1 - num2)
                  elif op == '*':
                      operand_stack.append(num1 * num2)
                  elif op == '/':
                      operand_stack.append(num1 / num2)
              operator_stack.append(elem)
      while len(operator_stack) > 0:
          op = operator_stack.pop()
          num2 = operand_stack.pop()
          num1 = operand_stack.pop()
          if op == '+':
              operand_stack.append(num1 + num2)
          elif op == '-':
              operand_stack.append(num1 - num2)
          elif op == '*':
              operand_stack.append(num1 * num2)
          elif op == '/':
              operand_stack.append(num1 / num2)
      if len(operand_stack) == 1:
          return operand_stack[0]
      return None

  def precedence(self, op):
      if op in ['+', '-']:
          return 1
      elif op in ['*', '/']:
          return 2
      else:
          return 0

  def handle_if_statement(self, line):
      condition, result = line.split("if ")[1].split(" then ")
      if condition:
          if eval(condition, self.variables):
              self.handle_print_statement("print " + result)

