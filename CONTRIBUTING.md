# Contributing to Exotel vSIP API Repository

Thank you for your interest in contributing to this project! This repository provides comprehensive implementations for Exotel vSIP APIs across multiple programming languages.

## 🤝 How to Contribute

### 1. **Fork and Clone**
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/exotel-vsip-trunk-Configuration-API.git
cd exotel-vsip-trunk-Configuration-API
```

### 2. **Create a Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. **Make Changes**
- Follow existing code patterns and conventions
- Maintain consistency across all language implementations
- Add appropriate error handling
- Include comprehensive documentation

### 4. **Test Your Changes**
```bash
# Run syntax validation
python3 test_api_files_exist.py

# Test specific language implementations
python3 tests/test_all_apis.py --verbose

# Test individual operations
python3 tests/test_all_apis.py --test your_new_test
```

### 5. **Commit and Push**
```bash
git add .
git commit -m "Add: Brief description of your changes"
git push origin feature/your-feature-name
```

### 6. **Create Pull Request**
- Open a pull request against the `main` branch
- Provide clear description of changes
- Reference any related issues

## 📋 Contribution Guidelines

### **Code Standards**

#### **Multi-Language Consistency**
- Maintain the same functionality across all 5 languages (cURL, Python, Go, Java, PHP)
- Use consistent variable names and patterns
- Follow language-specific conventions while maintaining overall consistency

#### **Error Handling**
- All implementations must include comprehensive error handling
- Use consistent error messages across languages
- Include proper HTTP status code handling
- Add logging for debugging purposes

#### **Documentation**
- Update README.md for any new features
- Add examples for new operations
- Update error code documentation if needed
- Include inline code comments for complex logic

### **Testing Requirements**

#### **All New Features Must Include:**
- ✅ Implementation in all 5 languages
- ✅ Test cases in the test suite
- ✅ Error handling tests
- ✅ Documentation updates
- ✅ Postman collection updates (if applicable)

#### **Testing Checklist:**
- [ ] Syntax validation passes (`python3 test_api_files_exist.py`)
- [ ] All existing tests still pass
- [ ] New functionality is tested
- [ ] Error scenarios are covered
- [ ] Documentation is updated

### **Types of Contributions Welcome**

#### **🔧 Code Contributions**
- New API endpoint implementations
- Bug fixes in existing code
- Performance improvements
- Enhanced error handling

#### **📚 Documentation**
- Improved setup guides
- Additional examples
- Error troubleshooting guides
- API usage documentation

#### **🧪 Testing**
- Additional test scenarios
- Edge case testing
- Performance testing
- Mock server improvements

#### **🌍 Language Support**
- Additional programming language implementations
- Language-specific optimizations
- Framework integrations

## 🚨 Important Notes

### **Security Considerations**
- **Never commit credentials** or API keys
- **Sanitize examples** - use placeholder values
- **Review .gitignore** before committing
- **Test with dummy data** only

### **API Compatibility**
- Ensure changes work with current Exotel API versions
- Test against real API endpoints when possible
- Maintain backward compatibility
- Document any breaking changes

### **Quality Standards**
- Code must be production-ready
- Include proper error handling
- Follow existing patterns and conventions
- Maintain comprehensive documentation

## 📞 Getting Help

### **Questions or Issues?**
- Check existing [Issues](https://github.com/Saurabhsharma209/exotel-vsip-trunk-Configuration-API/issues)
- Review [Documentation](README.md)
- Check [Error Reference](TRUNK_ERRORS_README.md)

### **Need Support?**
- Create a [GitHub Issue](https://github.com/Saurabhsharma209/exotel-vsip-trunk-Configuration-API/issues/new)
- Provide detailed description and steps to reproduce
- Include relevant code snippets and error messages

## 🏆 Recognition

Contributors will be recognized in:
- Repository contributors list
- Release notes for significant contributions
- Documentation credits

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

**Thank you for helping make this project better! 🚀** 