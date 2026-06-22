# To do

- [ ] Preserve every field in the VCF file, not just some of them.
- [x] Write a Makefile to generate the CSV output.
- [ ] Suppress output of fields if they are never used
- [ ] Add nickname column

# Test cases to add

- [ ] Add example of name with suffix and prefix
- [ ] Add example of version 3.0 with Unicode
- [ ] Add example of phone number with 'MOBILE' field

# Maybe do

- [ ] Check that the `vobject` library is installed.
    - [ ] Print a helpful error message if it isnt.
- [ ] Take `.vcf` files as arguments instead of just using `glob`.
- [ ] Send CSV to `stdout` instead of opening a file.
- [ ] Make phone numbers in the 123-456-7890 format instead of 1234567890 for better readability.
- [ ] Support vCard v4.0.
