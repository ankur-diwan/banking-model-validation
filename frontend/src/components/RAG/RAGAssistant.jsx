import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  IconButton,
  List,
  ListItem,
  CircularProgress,
  Chip,
  Avatar,
  Tooltip,
  Card,
  CardContent
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as AIIcon,
  Person as UserIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  ContentCopy as CopyIcon
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';

/**
 * RAG Assistant - AI-powered documentation assistant using watsonx.ai
 */
const RAGAssistant = ({ context = null }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions] = useState([
    'What are the key assumptions in this model?',
    'Explain the validation methodology',
    'What are the regulatory requirements?',
    'Summarize the model performance metrics'
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Simulate API call - replace with actual ragAPI.generateAnswer
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const aiMessage = {
        role: 'assistant',
        content: `Based on the documentation, ${input.toLowerCase().includes('assumption') ? 'the key assumptions include: 1) Data quality and completeness, 2) Stable economic conditions, 3) Representative training data' : 'I can help you with that. The validation methodology follows SR 11-7 guidelines and includes comprehensive testing of model assumptions, data quality, and performance metrics.'}`,
        sources: ['Model Documentation v2.1', 'SR 11-7 Guidelines'],
        confidence: 0.92,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        error: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };

  const handleCopy = (content) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AIIcon color="primary" />
          <Typography variant="h6">RAG Assistant</Typography>
          <Chip label="Powered by watsonx.ai" size="small" sx={{ ml: 'auto' }} />
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Ask questions about model documentation, validation requirements, and regulatory guidelines
        </Typography>
      </Paper>

      {/* Messages */}
      <Paper sx={{ flex: 1, p: 2, overflow: 'auto', mb: 2 }}>
        {messages.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <AIIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              How can I help you today?
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Try asking about model validation, regulatory requirements, or documentation
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
              {suggestions.map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  onClick={() => handleSuggestionClick(suggestion)}
                  clickable
                />
              ))}
            </Box>
          </Box>
        ) : (
          <List>
            {messages.map((message, index) => (
              <ListItem
                key={index}
                sx={{
                  flexDirection: 'column',
                  alignItems: message.role === 'user' ? 'flex-end' : 'flex-start',
                  mb: 2
                }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    gap: 1,
                    maxWidth: '80%',
                    flexDirection: message.role === 'user' ? 'row-reverse' : 'row'
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main'
                    }}
                  >
                    {message.role === 'user' ? <UserIcon /> : <AIIcon />}
                  </Avatar>
                  <Card
                    sx={{
                      bgcolor: message.role === 'user' ? 'primary.light' : 'background.paper',
                      flex: 1
                    }}
                  >
                    <CardContent>
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                      
                      {message.sources && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="caption" color="text.secondary">
                            Sources:
                          </Typography>
                          {message.sources.map((source, idx) => (
                            <Chip
                              key={idx}
                              label={source}
                              size="small"
                              sx={{ mr: 0.5, mt: 0.5 }}
                            />
                          ))}
                        </Box>
                      )}

                      {message.confidence && (
                        <Box sx={{ mt: 1 }}>
                          <Chip
                            label={`Confidence: ${(message.confidence * 100).toFixed(0)}%`}
                            size="small"
                            color={message.confidence > 0.8 ? 'success' : 'warning'}
                          />
                        </Box>
                      )}

                      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                        <Tooltip title="Copy">
                          <IconButton size="small" onClick={() => handleCopy(message.content)}>
                            <CopyIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        {message.role === 'assistant' && !message.error && (
                          <>
                            <Tooltip title="Helpful">
                              <IconButton size="small">
                                <ThumbUpIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Not helpful">
                              <IconButton size="small">
                                <ThumbDownIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </>
                        )}
                      </Box>
                    </CardContent>
                  </Card>
                </Box>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  {message.timestamp.toLocaleTimeString()}
                </Typography>
              </ListItem>
            ))}
            {loading && (
              <ListItem>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Avatar sx={{ bgcolor: 'secondary.main' }}>
                    <AIIcon />
                  </Avatar>
                  <CircularProgress size={24} />
                  <Typography variant="body2" color="text.secondary">
                    Thinking...
                  </Typography>
                </Box>
              </ListItem>
            )}
            <div ref={messagesEndRef} />
          </List>
        )}
      </Paper>

      {/* Input */}
      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Ask a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={loading}
          />
          <Button
            variant="contained"
            onClick={handleSend}
            disabled={!input.trim() || loading}
            endIcon={<SendIcon />}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default RAGAssistant;

// Made with Bob
