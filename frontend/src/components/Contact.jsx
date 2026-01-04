import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { useToast } from '../hooks/use-toast';

const Contact = ({ data }) => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock submission
    toast({
      title: "Message Sent!",
      description: "Thank you for reaching out. I'll get back to you soon.",
    });
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <section className="section-container" id="contact">
      <div className="section-content">
        <div className="section-header">
          <h2 className="section-title">Get in Touch</h2>
          <p className="section-subtitle">Let's connect for collaboration, research, or consultation</p>
        </div>
        
        <div className="contact-grid">
          <div className="contact-info">
            <h3 className="contact-info-title">Contact Information</h3>
            
            <div className="contact-item">
              <div className="contact-icon">
                <Mail className="w-5 h-5" />
              </div>
              <div>
                <div className="contact-label">Email</div>
                <a href={`mailto:${data.email}`} className="contact-value">{data.email}</a>
              </div>
            </div>
            
            <div className="contact-item">
              <div className="contact-icon">
                <Phone className="w-5 h-5" />
              </div>
              <div>
                <div className="contact-label">Phone</div>
                <a href={`tel:${data.phone}`} className="contact-value">{data.phone}</a>
              </div>
            </div>
            
            <div className="contact-item">
              <div className="contact-icon">
                <MapPin className="w-5 h-5" />
              </div>
              <div>
                <div className="contact-label">Location</div>
                <div className="contact-value">{data.location}</div>
              </div>
            </div>
            
            <div className="contact-affiliation">
              <h4 className="affiliation-title">Current Affiliation</h4>
              <p className="affiliation-text">SGT University</p>
              <p className="affiliation-text">CV Raman Block, Budhera</p>
              <p className="affiliation-text">Haryana, 122505</p>
            </div>
          </div>
          
          <div className="contact-form-wrapper">
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-group">
                <label htmlFor="name" className="form-label">Name</label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Your name"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email</label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="your.email@example.com"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="subject" className="form-label">Subject</label>
                <Input
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  placeholder="What is this regarding?"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="message" className="form-label">Message</label>
                <Textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Your message..."
                  rows={5}
                  required
                />
              </div>
              
              <Button type="submit" className="btn-primary w-full">
                <Send className="w-4 h-4 mr-2" />
                Send Message
              </Button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
